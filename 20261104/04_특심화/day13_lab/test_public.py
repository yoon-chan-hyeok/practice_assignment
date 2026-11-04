"""특심화 공개 테스트: 정확성·재현성·실패 의미를 검사합니다. 보고서 해석은 채점하지 않습니다."""
from pathlib import Path
from queue import Queue
from threading import Event
import csv,hashlib,json,shutil,tempfile,unittest
from unittest.mock import patch
import cv2
import numpy as np
from contracts import normalize_bgr
from geometry import Letterbox
from quality import pareto_indices,mask_metrics
from augmentation import augment
from cache import cache_key,can_reuse
from engine import run_images
from video_pipeline import offer_frame,process_frame,run_video

BASE=Path(__file__).resolve().parent
CONFIG={"size":[224,224],"seed":42,"blur":3,"canny":[80,160]}

def fixture():
    a=np.arange(12*16*3,dtype=np.uint8).reshape(12,16,3)
    a[2,3]=[0,0,255]
    return a

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

class ContractTests(unittest.TestCase):
    def test_copy_and_strides(self):
        x=fixture();view=x[:,::2];before=x.copy();out,info=normalize_bgr(view)
        self.assertTrue(out.flags.c_contiguous);self.assertFalse(np.shares_memory(out,x));np.testing.assert_array_equal(out,view)
        out[:]=0;np.testing.assert_array_equal(x,before);self.assertFalse(info['shares_memory'])
    def test_known_bgr_patch(self):
        image=fixture();normalize_bgr(image,{(2,3):(0,0,255)})
        with self.assertRaises(ValueError):normalize_bgr(image[:,:,::-1],{(2,3):(0,0,255)})
    def test_no_universal_channel_guess(self):
        image=fixture()[:,:,::-1];out,_=normalize_bgr(image);np.testing.assert_array_equal(out,image)
    def test_invalid_image_contract(self):
        for x in [fixture().astype(np.float32),fixture().astype(np.uint16)]:
            with self.assertRaises(TypeError):normalize_bgr(x)
        for x in [np.zeros((0,2,3),np.uint8),np.zeros((3,4),np.uint8),np.zeros((3,4,4),np.uint8)]:
            with self.assertRaises(ValueError):normalize_bgr(x)
    def test_patch_bounds(self):
        with self.assertRaises(ValueError):normalize_bgr(fixture(),{(500,0):(0,0,0)})

class GeometryTests(unittest.TestCase):
    def test_output_size_and_padding(self):
        image=np.ones((13,31,3),np.uint8)*255;out,m=Letterbox((223,225))(image)
        self.assertEqual(out.shape,(225,223,3));l,t,r,b=m.pad_ltrb
        self.assertEqual(l+m.resized_wh[0]+r,223);self.assertEqual(t+m.resized_wh[1]+b,225)
        self.assertEqual(out.dtype,np.uint8)
    def test_actual_scales_and_roundtrip(self):
        rng=np.random.default_rng(3)
        for _ in range(30):
            h,w=(int(x) for x in rng.integers(1,100,2));image=np.zeros((h,w,3),np.uint8)
            _,m=Letterbox((223,225))(image)
            self.assertEqual(m.scale_xy,(m.resized_wh[0]/w,m.resized_wh[1]/h))
            p=rng.random((10,2))*[w,h];mapped=Letterbox.map_points(p,m)
            np.testing.assert_allclose(Letterbox.map_points(mapped,m,True),p,atol=1e-9)
    def test_box_edges(self):
        _,m=Letterbox((225,223))(np.zeros((240,320,3),np.uint8))
        box=np.array([[0,0,320,240],[10,20,100,120]],float)
        mapped=Letterbox.map_boxes(box,m);back=Letterbox.map_boxes(mapped,m,True)
        np.testing.assert_allclose(back,box,atol=1e-9)
    def test_single_pixel(self):
        out,m=Letterbox((1,7))(np.ones((1,1,3),np.uint8));self.assertEqual(out.shape,(7,1,3))
    def test_empty_points(self):
        _,m=Letterbox()(fixture());self.assertEqual(Letterbox.map_points(np.empty((0,2)),m).shape,(0,2))
    def test_invalid_coordinates(self):
        _,m=Letterbox()(fixture())
        with self.assertRaises(ValueError):Letterbox((0,2))
        with self.assertRaises(ValueError):Letterbox.map_points([[float('nan'),0]],m)
        with self.assertRaises(ValueError):Letterbox.map_boxes([[2,0,1,1]],m)

class QualityTests(unittest.TestCase):
    def test_pareto_dominance_and_ties(self):
        rows=[{'mse':2,'median_ms':3},{'mse':1,'median_ms':4},{'mse':3,'median_ms':4},{'mse':2,'median_ms':3}]
        saved=json.dumps(rows);self.assertEqual(pareto_indices(rows),[0,1,3]);self.assertEqual(json.dumps(rows),saved)
    def test_pareto_empty(self):self.assertEqual(pareto_indices([]),[])
    def test_pareto_invalid(self):
        for v in [-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):pareto_indices([{'mse':v,'median_ms':1}])
    def test_mask_metrics(self):
        truth=np.zeros((10,10),np.uint8);truth[1:4,1:4]=255;truth[6:8,6:8]=255
        mask=truth.copy();mask[1,1]=0;r=mask_metrics(mask,truth)
        self.assertAlmostEqual(r['iou'],12/13);self.assertEqual(r['components'],2);self.assertEqual(r['component_areas'],[4,8])
    def test_empty_foreground(self):
        z=np.zeros((3,4),np.uint8);r=mask_metrics(z,z)
        self.assertEqual(r['iou'],1.0);self.assertEqual(r['components'],0)
    def test_invalid_mask(self):
        with self.assertRaises(ValueError):mask_metrics(np.ones((3,4),np.uint8),np.zeros((3,4),np.uint8))
        with self.assertRaises(ValueError):mask_metrics(np.zeros((3,4),np.uint8),np.zeros((4,4),np.uint8))
        with self.assertRaises(TypeError):mask_metrics(np.zeros((3,4),float),np.zeros((3,4),np.uint8))

class AugmentTests(unittest.TestCase):
    def test_repeat_and_original(self):
        x=fixture();original=x.copy();a,ma=augment(x,42,'a');b,mb=augment(x,42,'a')
        np.testing.assert_array_equal(a,b);np.testing.assert_array_equal(x,original);self.assertEqual(ma,mb)
    def test_order_independent(self):
        x=fixture();forward={id:augment(x,42,id)[0] for id in ['a','b','c']}
        for id in ['c','a','b']:np.testing.assert_array_equal(forward[id],augment(x,42,id)[0])
    def test_valid_test_noop(self):
        for split in ['valid','test']:
            x=fixture();out,m=augment(x,0,'a',split=split)
            np.testing.assert_array_equal(out,x);self.assertFalse(np.shares_memory(out,x));self.assertFalse(m['applied'])
    def test_global_rng_unchanged(self):
        state=np.random.get_state();augment(fixture(),42,'a');after=np.random.get_state()
        self.assertEqual(state[0],after[0]);np.testing.assert_array_equal(state[1],after[1]);self.assertEqual(state[2:],after[2:])
    def test_label_policy(self):
        for i in range(15):
            out,m=augment(fixture(),42,str(i),allow_flip=False,allow_rotate=False)
            self.assertFalse(m['flip']);self.assertEqual(m['angle'],0);self.assertTrue(-25<=m['beta']<=25)
    def test_invalid_split(self):
        with self.assertRaises(ValueError):augment(fixture(),42,'a',split='validation_typo')

class QueueTests(unittest.TestCase):
    def test_drop_keeps_older(self):
        q=Queue(1);q.put('first');self.assertFalse(offer_frame(q,'new','drop_latest',Event()));self.assertEqual(q.get(),'first')
    def test_block_success(self):
        q=Queue(1);self.assertTrue(offer_frame(q,'ok','block',Event()));self.assertEqual(q.get(),'ok')
    def test_cancel(self):
        q=Queue(1);q.put(1);cancel=Event();cancel.set();self.assertFalse(offer_frame(q,2,'block',cancel))
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):offer_frame(Queue(1),1,'drop_oldest',Event())
    def test_frame_transform(self):
        x=fixture();original=x.copy();out=process_frame(x)
        self.assertEqual(out.shape,(120,160,3));self.assertEqual(out.dtype,np.uint8);np.testing.assert_array_equal(x,original)
        np.testing.assert_array_equal(out,process_frame(x))

class CacheTests(unittest.TestCase):
    def test_canonical_order(self):
        self.assertEqual(cache_key(b'a',{'b':1,'a':2},'x','train'),cache_key(b'a',{'a':2,'b':1},'x','train'))
    def test_input_or_config_changes(self):
        one=cache_key(b'a',{'seed':1},'x','train')
        self.assertNotEqual(one,cache_key(b'b',{'seed':1},'x','train'));self.assertNotEqual(one,cache_key(b'a',{'seed':2},'x','train'))
        self.assertNotEqual(one,cache_key(b'a',{'seed':1},'x','valid'))
    def test_reuse_checks_decode_hash_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'x.png';cv2.imwrite(str(path),fixture());r={'status':'ok','key':'key','output_sha256':digest(path),'shape':list(fixture().shape),'dtype':'uint8'}
            self.assertTrue(can_reuse(r,'key',path));self.assertFalse(can_reuse(r,'other',path))
            self.assertFalse(can_reuse({**r,'shape':[1,1,3]},'key',path))
            path.write_bytes(b'not png');self.assertFalse(can_reuse(r,'key',path))
    def test_missing_failed(self):
        self.assertFalse(can_reuse(None,'k','not-present'))
        self.assertFalse(can_reuse({'status':'failed'},'k','not-present'))

class IntegrationTests(unittest.TestCase):
    def test_serial_parallel_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=run_images(BASE/'data',Path(tmp)/'one',CONFIG,1)
            b=run_images(BASE/'data',Path(tmp)/'two',CONFIG,2)
            self.assertEqual(a['ok'],6);self.assertEqual(a['failed'],0);self.assertEqual(b['ok'],6)
            for id in a['records']:
                self.assertEqual(a['records'][id]['output_sha256'],b['records'][id]['output_sha256'])
                self.assertEqual(a['records'][id]['settings'],b['records'][id]['settings'])
            resumed=run_images(BASE/'data',Path(tmp)/'two',CONFIG,2,True);self.assertEqual(resumed['reused'],6)
    def test_tampered_output_is_recomputed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';a=run_images(BASE/'data',out,CONFIG)
            (out/'img_01.png').write_bytes(b'broken')
            b=run_images(BASE/'data',out,CONFIG,resume=True);self.assertEqual(b['reused'],5);self.assertEqual(b['ok'],6)
            self.assertEqual(a['records']['img_01']['output_sha256'],b['records']['img_01']['output_sha256'])
    def test_processing_setting_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';run_images(BASE/'data',out,CONFIG)
            result=run_images(BASE/'data',out,{**CONFIG,'seed':43},resume=True);self.assertEqual(result['reused'],0)
    def test_corrupt_source_failure_then_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp)/'data';shutil.copytree(BASE/'data',data);path=data/'images/train_01.png';original=path.read_bytes();path.write_bytes(b'bad data')
            out=Path(tmp)/'out';a=run_images(data,out,CONFIG);self.assertEqual(a['failed'],1);self.assertEqual(a['ok'],5)
            path.write_bytes(original);b=run_images(data,out,CONFIG,resume=True);self.assertEqual(b['ok'],6);self.assertEqual(b['reused'],5)
    def test_protect_data_root(self):
        with self.assertRaises(ValueError):run_images(BASE/'data',BASE/'data'/'outputs',CONFIG)
    def test_original_bytes_preserved(self):
        hashes={p.relative_to(BASE/'data').as_posix():digest(p) for p in (BASE/'data').rglob('*') if p.is_file()}
        with tempfile.TemporaryDirectory() as tmp:run_images(BASE/'data',Path(tmp)/'out',CONFIG)
        after={p.relative_to(BASE/'data').as_posix():digest(p) for p in (BASE/'data').rglob('*') if p.is_file()}
        self.assertEqual(hashes,after)
    def test_video_no_drop(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=run_video(BASE/'data/sample.avi',Path(tmp)/'block.avi')
            self.assertEqual((r['decoded'],r['written'],r['dropped']),(48,48,0));self.assertEqual(r['output_duration_s'],4.0)
            self.assertEqual([x['source_index'] for x in r['frame_map']],list(range(48)))
    def test_video_drop_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=run_video(BASE/'data/sample.avi',Path(tmp)/'drop.avi',policy='drop_latest',processing_delay_s=.003)
            self.assertEqual(r['decoded'],r['written']+r['dropped']);self.assertLessEqual(r['queue_in_sampled_peak'],2)
            ids=[x['source_index'] for x in r['frame_map']];self.assertEqual(ids,sorted(set(ids)))
            self.assertEqual(set(ids)|set(r['dropped_indices']),set(range(48)))
    def test_worker_error_propagates(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('video_pipeline.process_frame',side_effect=ValueError('injected failure')):
                with self.assertRaises(RuntimeError):run_video(BASE/'data/sample.avi',Path(tmp)/'failed.avi')
    def test_optional_lossless_codec(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'ffv1.avi';probe=cv2.VideoWriter(str(out),cv2.VideoWriter_fourcc(*'FFV1'),12,(160,120))
            supported=probe.isOpened();probe.release()
            if not supported:self.skipTest('FFV1 인코더가 없는 환경')
            r=run_video(BASE/'data/sample.avi',out,codec='FFV1');self.assertEqual(r['written'],48)
            cap=cv2.VideoCapture(str(BASE/'data/sample.avi'));_,raw=cap.read();cap.release()
            cap=cv2.VideoCapture(str(out));_,decoded=cap.read();cap.release()
            np.testing.assert_array_equal(decoded,process_frame(raw))

if __name__=='__main__':
    cv2.setNumThreads(1)
    unittest.main(verbosity=2)
