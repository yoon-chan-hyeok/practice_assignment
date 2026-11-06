"""특심화 공개 테스트. 완료하지 않은 TODO는 실패합니다. 외부 YOLO 검증은 별도 표시합니다."""
from pathlib import Path
import sys,unittest,tempfile,json,copy,time,importlib.util
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geometry import Box,iou_matrix,class_nms
from metrics import match_predictions,ap101,evaluate
from audit import audit_label,audit_dataset
from tracking import IoUTracker,count_id_switches
from artifacts import reusable,run_artifacts,ordered_map,canonical_hash,sha256,compare_regression,atomic_json


def gt(image='a',cls=0,box=(0,0,10,10)):
    return dict(image_id=image,class_id=cls,**dict(zip(['x1','y1','x2','y2'],box)))
def pred(image='a',cls=0,score=.9,box=(0,0,10,10)):
    return dict(gt(image,cls,box),confidence=score)

class Coordinates(unittest.TestCase):
    def test_roundtrip_nonsquare(self):
        b=Box(20,10,80,40);v=b.to_yolo(160,80);np.testing.assert_allclose(v,[.3125,.3125,.375,.375]);self.assertEqual(Box.from_yolo(v,160,80),b)
    def test_negative_size(self):
        with self.assertRaises(ValueError):Box(0,0,1,1).to_yolo(0,20)
    def test_float_image_size(self):
        with self.assertRaises(ValueError):Box(0,0,1,1).to_yolo(20.5,20)
    def test_zero_area(self):
        with self.assertRaises(ValueError):Box(0,0,0,1)
    def test_nan(self):
        with self.assertRaises(ValueError):Box(0,0,float('nan'),1)
    def test_clip(self):self.assertEqual(Box(-1,-2,12,14).clip(10,10),Box(0,0,10,10))
    def test_clip_empty(self):
        with self.assertRaises(ValueError):Box(11,11,12,12).clip(10,10)
    def test_yolo_edges(self):
        with self.assertRaises(ValueError):Box.from_yolo([.95,.5,.4,.4],100,80)
    def test_new_output(self):
        b=Box(0,0,10,10);v=b.to_yolo(20,20);v[0]=999;self.assertEqual(b.x1,0)

class Overlap(unittest.TestCase):
    def test_identity(self):self.assertEqual(iou_matrix([[0,0,10,10]],[[0,0,10,10]])[0,0],1)
    def test_touch(self):self.assertEqual(iou_matrix([[0,0,10,10]],[[10,0,20,10]])[0,0],0)
    def test_example(self):self.assertAlmostEqual(iou_matrix([[0,0,2,2]],[[1,1,3,3]])[0,0],1/7)
    def test_empty(self):self.assertEqual(iou_matrix([],[[0,0,1,1]]).shape,(0,1))
    def test_no_mutation(self):
        a=np.array([[0.,0,10,10]]);old=a.copy();iou_matrix(a,a);np.testing.assert_array_equal(a,old)
    def test_invalid(self):
        with self.assertRaises(ValueError):iou_matrix([[1,1,0,0]],[])
    def test_nms_same_class(self):self.assertEqual(class_nms([[0,0,10,10]]*2,[.9,.8],[0,0],.5),[0])
    def test_nms_different_class(self):self.assertEqual(class_nms([[0,0,10,10]]*2,[.9,.8],[0,1],.5),[0,1])
    def test_nms_tie_stable(self):self.assertEqual(class_nms([[0,0,10,10]]*2,[.8,.8],[0,0],.5),[0])
    def test_nms_equal_threshold(self):self.assertEqual(class_nms([[0,0,10,10]]*2,[.8,.7],[0,0],1),[0,1])
    def test_nms_empty(self):self.assertEqual(class_nms(np.empty((0,4)),[],np.array([],int)),[])
    def test_nms_bad_score(self):
        with self.assertRaises(ValueError):class_nms([[0,0,1,1]],[float('nan')],[0])

class DetectionMetrics(unittest.TestCase):
    def test_exact(self):self.assertEqual(match_predictions([pred()],[gt()])[1],dict(tp=1,fp=0,fn=0))
    def test_duplicate(self):self.assertEqual(match_predictions([pred(),pred(score=.8)],[gt()])[1],dict(tp=1,fp=1,fn=0))
    def test_class_mismatch(self):self.assertEqual(match_predictions([pred(cls=1)],[gt()])[1],dict(tp=0,fp=1,fn=1))
    def test_image_mismatch(self):self.assertEqual(match_predictions([pred(image='b')],[gt()])[1],dict(tp=0,fp=1,fn=1))
    def test_empty_pred(self):self.assertEqual(match_predictions([],[gt()])[1]['fn'],1)
    def test_empty_gt(self):self.assertEqual(match_predictions([pred()],[])[1]['fp'],1)
    def test_score_order(self):
        r,_=match_predictions([pred(score=.4),pred(score=.9)],[gt()]);self.assertEqual(r[0]['prediction_index'],1);self.assertEqual(r[0]['tp'],1)
    def test_unchanged(self):
        p=[pred()];g=[gt()];old=copy.deepcopy((p,g));match_predictions(p,g);self.assertEqual((p,g),old)
    def test_ap_perfect(self):self.assertEqual(ap101([1,1],2),1.)
    def test_ap_none(self):self.assertIsNone(ap101([],0))
    def test_ap_empty(self):self.assertEqual(ap101([],2),0.)
    def test_ap_partial_recall(self):self.assertAlmostEqual(ap101([1],2),51/101)
    def test_ap_fp_first(self):self.assertEqual(ap101([0,1],1),.5)
    def test_ap_duplicate_after_tp(self):self.assertEqual(ap101([1,0],1),1.)
    def test_ap_not_binary(self):
        with self.assertRaises(ValueError):ap101([.5],1)
    def test_map_classes(self):
        rows=evaluate([pred()],[gt()],classes=[0,1],thresholds=[.5]);self.assertEqual(rows[0]['ap'],1);self.assertIsNone(rows[1]['ap'])

class Audit(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.p=Path(self.temp.name)/'a.txt'
    def tearDown(self):self.temp.cleanup()
    def check(self,text):self.p.write_text(text);return audit_label(self.p,160,128,['a','b','c'])
    def test_normal(self):self.assertEqual(self.check('0 .5 .5 .2 .2')['objects'],1)
    def test_empty_is_negative(self):self.assertEqual(self.check(''),dict(objects=0,errors=[]))
    def test_missing(self):self.assertEqual(audit_label(self.p,160,128,['a'])['errors'],['missing_label'])
    def test_edge_overflow(self):self.assertTrue(self.check('0 .95 .5 .4 .4')['errors'])
    def test_noninteger_class(self):self.assertTrue(self.check('0.5 .5 .5 .2 .2')['errors'])
    def test_duplicate(self):self.assertTrue(self.check('0 .5 .5 .2 .2\n0 .5 .5 .2 .2')['errors'])
    def test_nan(self):self.assertTrue(self.check('0 nan .5 .2 .2')['errors'])
    def test_columns(self):self.assertTrue(self.check('0 .5 .5 .2')['errors'])

class Tracking(unittest.TestCase):
    def test_same_object(self):
        t=IoUTracker();self.assertEqual(t.update('a',0,[[0,0,10,10]],[0]),[1]);self.assertEqual(t.update('a',1,[[1,0,11,10]],[0]),[1])
    def test_stream_isolation(self):
        t=IoUTracker();self.assertEqual(t.update('a',0,[[0,0,10,10]],[0]),[1]);self.assertEqual(t.update('b',0,[[0,0,10,10]],[0]),[1])
    def test_new_class(self):
        t=IoUTracker();t.update('a',0,[[0,0,10,10]],[0]);self.assertEqual(t.update('a',1,[[0,0,10,10]],[1]),[2])
    def test_gap_expiry(self):
        t=IoUTracker(max_gap=1);t.update('a',0,[[0,0,10,10]],[0]);t.update('a',1,[],[]);self.assertEqual(t.update('a',2,[[0,0,10,10]],[0]),[2])
    def test_frame_order(self):
        t=IoUTracker();t.update('a',0,[],[])
        with self.assertRaises(ValueError):t.update('a',0,[],[])
    def test_reset(self):
        t=IoUTracker();t.update('a',5,[[0,0,10,10]],[0]);t.reset('a');self.assertEqual(t.update('a',0,[[0,0,10,10]],[0]),[1])
    def test_one_to_one(self):
        t=IoUTracker();t.update('a',0,[[0,0,10,10]],[0]);self.assertEqual(t.update('a',1,[[0,0,10,10],[0,0,10,10]],[0,0]),[1,2])
    def test_gt_switch_metric(self):
        g=[dict(frame=i,gt_id=1,class_id=0,x1=0,y1=0,x2=10,y2=10) for i in range(2)]
        p=[dict(frame=i,track_id=i+1,class_id=0,x1=0,y1=0,x2=10,y2=10) for i in range(2)]
        self.assertEqual(count_id_switches(g,p)['continuous_match_id_switches'],1)

class Artifacts(unittest.TestCase):
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name);self.source=self.root/'input.txt';self.source.write_text('one')
    def tearDown(self):self.t.cleanup()
    def test_stable_hash(self):self.assertEqual(canonical_hash({'a':1,'b':2}),canonical_hash({'b':2,'a':1}))
    def test_reuse_and_corruption(self):
        out=self.root/'out';fn=lambda p:{'text':p.read_text()}
        self.assertEqual(run_artifacts([self.source],out,{'backend':'fixture'},fn)[0][1],'success')
        self.assertEqual(run_artifacts([self.source],out,{'backend':'fixture'},fn)[0][1],'reused')
        (out/'input.json').write_text('broken')
        self.assertEqual(run_artifacts([self.source],out,{'backend':'fixture'},fn)[0][1],'success')
    def test_changed_source(self):
        out=self.root/'out';fn=lambda p:{'text':p.read_text()};run_artifacts([self.source],out,{},fn)
        self.source.write_text('two');self.assertEqual(run_artifacts([self.source],out,{},fn)[0][1],'success')
    def test_changed_config(self):
        out=self.root/'out';fn=lambda p:1;run_artifacts([self.source],out,{'x':1},fn)
        self.assertEqual(run_artifacts([self.source],out,{'x':2},fn)[0][1],'success')
    def test_failed_recovery(self):
        def bad(_):raise RuntimeError('intentional')
        out=self.root/'out';self.assertEqual(run_artifacts([self.source],out,{},bad)[0][1],'failed')
        self.assertEqual(run_artifacts([self.source],out,{},lambda p:1)[0][1],'success')
    def test_ordered_workers(self):
        def f(i):time.sleep((5-i)*.001);return i*2
        self.assertEqual(list(ordered_map(f,list(range(5)),2,2)),[0,2,4,6,8])
    def test_none_item(self):self.assertEqual(list(ordered_map(lambda x:x,[1,None,2],1,1)),[1,None,2])
    def test_worker_error(self):
        def f(i):raise ValueError('worker')
        with self.assertRaises(ValueError):list(ordered_map(f,[1],1,1))
    def test_worker_setting(self):
        with self.assertRaises(ValueError):list(ordered_map(lambda x:x,[1],0,1))
    def test_perf_equal_scope(self):
        a=dict(scope='geometry',device='cpu',imgsz=160,batch=1,model_sha='x',median_ms=10)
        self.assertTrue(compare_regression(a,dict(a,median_ms=11))['passed']);self.assertFalse(compare_regression(a,dict(a,median_ms=15))['passed'])
    def test_perf_different_scope(self):
        a=dict(scope='geometry',device='cpu',imgsz=160,batch=1,model_sha='x',median_ms=10)
        self.assertFalse(compare_regression(a,dict(a,device='cuda'))['comparable'])

    def test_duplicate_output_stem(self):
        other=self.root/'input.csv';other.write_text('another')
        with self.assertRaises(ValueError):
            run_artifacts([self.source,other],self.root/'out',{},lambda p:1)
    def test_missing_benchmark_contract(self):
        self.assertFalse(compare_regression({'median_ms':1},{'median_ms':1})['comparable'])
    def test_nonfinite_benchmark(self):
        a=dict(scope='geometry',device='cpu',imgsz=160,batch=1,model_sha='x',median_ms=10)
        for value in [float('nan'),float('inf'),0,-1]:
            with self.assertRaises(ValueError):compare_regression(a,dict(a,median_ms=value))

ULTRA=importlib.util.find_spec('ultralytics') is not None
MODEL=Path(__file__).resolve().parent/'data/demo.pt'
class OptionalYOLO(unittest.TestCase):
    @unittest.skipUnless(ULTRA and MODEL.exists(),'실제 ultralytics·준비 모델이 필요합니다. 제작 시 미검증.')
    def test_real_predict(self):
        from ultralytics import YOLO
        m=YOLO(str(MODEL));r=m.predict(source=str(MODEL.parent/'scene.png'),imgsz=160,device='cpu',verbose=False)
        self.assertEqual(len(r),1);self.assertEqual(r[0].boxes.xyxy.shape[1],4)
    @unittest.skipUnless(ULTRA and MODEL.exists(),'실제 ultralytics·준비 모델이 필요합니다. 제작 시 미검증.')
    def test_real_track(self):
        from ultralytics import YOLO
        rows=list(YOLO(str(MODEL)).track(source=str(MODEL.parent/'demo.avi'),tracker='bytetrack.yaml',imgsz=160,device='cpu',stream=True,persist=False,verbose=False))
        self.assertEqual(len(rows),30)

if __name__=='__main__':unittest.main(verbosity=2)
