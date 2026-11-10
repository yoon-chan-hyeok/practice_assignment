"""특심화: 결과 재사용은 존재 여부가 아닌 입력·설정·출력 무결성에 근거합니다."""
from pathlib import Path
import json, hashlib, os, re, uuid, time
import cv2
from contracts import OCRPage
from extractors import extract_invoice
from policy import parse_vlm, decide
from backends import make_backend


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
        os.replace(tmp,path)
    finally:
        if tmp.exists():tmp.unlink()

def cache_valid(entry,input_sha,config_sha,artifact):
    # S09 요구사항
    # 성공 상태, 원본 hash, 설정+schema+backend fixture+구현 hash 일치,
    # 출력 파일 존재 및 output_sha256 일치 모두 필요. 하나라도 실패하면 False.
    # failed 항목은 재사용 금지. JSON 파싱 성공도 필요. 예외는 False로 돌린다.
    # artifact는 호출자가 정한 경로만 사용한다. entry에서 받은 임의 경로를 열지 않는다.
# TODO S09
    raise NotImplementedError('S09: validated artifact reuse')
# TODO 끝 S09


def run_documents(data_dir,output_dir,config):
    data_dir=Path(data_dir);output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    lesson=json.loads((data_dir/'lesson.json').read_text(encoding='utf-8'))
    # 여기서 truth·reference_text는 backend나 추출 함수에 전달하지 않습니다.
    documents={k:{'file':v['file'],'ocr':v['ocr'],'mock_vlm':v['mock_vlm']} for k,v in lesson['documents'].items()}
    backend=make_backend(config['backend'],documents,config.get('model_dir'))
    code_hash=digest({p.name:file_hash(p) for p in sorted(Path(__file__).parent.glob('*.py'))})
    cfg_hash=digest({'config':config,'schema':'invoice-v1','code':code_hash,'fixtures':documents,'model_fingerprint':getattr(backend,'fingerprint',None)})
    old_path=output_dir/'manifest.json'
    old=json.loads(old_path.read_text(encoding='utf-8')) if old_path.exists() else {}
    entries={};counts={'processed':0,'reused':0,'failed':0}
    for document_id,doc in sorted(documents.items()):
        if not re.fullmatch(r'[A-Za-z0-9_-]+',document_id):raise ValueError('unsafe id')
        image_path=(data_dir/doc['file']).resolve()
        if not image_path.is_relative_to(data_dir.resolve()):raise ValueError('image path outside data')
        path=output_dir/(document_id+'.json')
        sha=file_hash(image_path)
        if cache_valid(old.get(document_id),sha,cfg_hash,path):
            entries[document_id]=old[document_id];counts['reused']+=1;continue
        try:
            if doc['ocr']['image_sha256']!=sha:raise ValueError('recorded OCR does not match input image')
            image=cv2.imread(str(image_path))
            if image is None:raise ValueError('image decode failed')
            page=OCRPage.from_tokens(doc['ocr']['tokens'],image.shape[1],image.shape[0])
            extracted=extract_invoice(page,document_id)
            answer=backend.ask(document_id,image_path)
            parsed=parse_vlm(answer['raw'])
            result={'document_id':document_id,'schema_version':'invoice-v1','ocr_backend':'recorded_tesseract','vlm_backend':answer['backend'],'model_id':answer['model_id'],'inference_ms':answer['latency_ms'],'fields':decide(extracted['fields'],parsed,config['min_confidence'])}
            atomic_json(path,result)
            entries[document_id]={'status':'success','input_sha256':sha,'config_sha256':cfg_hash,'output_sha256':file_hash(path)}
            counts['processed']+=1
        except Exception as error:
            path.unlink(missing_ok=True)  # 현재 입력에 대응하지 않는 과거 결과를 공개하지 않습니다.
            # 원문이나 예외 message에 개인정보가 들어갈 수 있어 로그는 유형만 기록합니다.
            entries[document_id]={'status':'failed','input_sha256':sha,'config_sha256':cfg_hash,'error_type':type(error).__name__}
            counts['failed']+=1
    atomic_json(old_path,entries)
    atomic_json(output_dir/'run_counts.json',counts)
    return counts
