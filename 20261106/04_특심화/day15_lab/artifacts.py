"""특심화: 처리 결과를 해시로 확인하고, 성공 완료 파일만 재사용한다."""
from pathlib import Path
import json,hashlib,os,tempfile,math
from concurrent.futures import ThreadPoolExecutor


def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical_hash(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def atomic_json(path, value):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=p.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.flush();os.fsync(f.fileno())
        os.replace(name,p)
    finally:
        if os.path.exists(name):os.unlink(name)


def reusable(record,input_path,config,output_path):
    # >>> X08
    # 요구: record.status=='success'이고 input/config/output SHA256이 모두 같을 때만 True.
    # record 없음·출력 없음·파일 손상·설정 변경이면 False. '파일 있음'만으로 성공 처리 금지.
    # JSON 설정의 키 순서는 결과에 영향을 주면 안 된다. 원본을 변경하지 않는다.
    raise NotImplementedError("TODO X08를 구현하세요.")
    # <<< X08


def ordered_map(function,items,workers=2,max_pending=4):
    # >>> X09
    # 요구: workers>=1, max_pending>=workers. 입력 순서와 동일한 출력 순서.
    # 동시에 제출되어 아직 회수되지 않은 future를 max_pending 이하로 제한한다.
    # worker 예외는 main에 전파하고 나머지 작업을 취소/종료한다. 자체 큐 deadlock 금지.
    # generator라 소비가 끝나거나 중단되어도 executor를 정리한다. 외부 함수의 무한 실행은 범위 밖.
    # 모델/Tracker 하나를 여러 worker가 공유하는 용도로 사용하지 않는다.
    raise NotImplementedError("TODO X09를 구현하세요.")
    # <<< X09


def run_artifacts(inputs,output_dir,config,processor):
    """processor(input_path) -> JSON 직렬화 가능한 값. 실제 backend 명칭은 config에 기록한다."""
    # 제공 코드: 서로 다른 입력이 같은 출력 이름을 덮어쓰지 않도록 먼저 차단한다.
    sources=list(map(Path,inputs))
    if len({p.stem.casefold() for p in sources}) != len(sources):
        raise ValueError('출력 파일 이름 충돌: 서로 다른 입력 stem을 사용하세요.')
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);mp=out/'manifest.json' 
    manifest=json.loads(mp.read_text(encoding='utf-8')) if mp.exists() else {}
    emitted=[]
    for source in sources:
        dest=out/(source.stem+'.json')
        old=manifest.get(source.name)
        if reusable(old,source,config,dest):emitted.append((source.name,'reused'));continue
        try:
            result=processor(source);atomic_json(dest,result)
            record=dict(status='success',input_sha=sha256(source),config_sha=canonical_hash(config),output_sha=sha256(dest),backend=config.get('backend','unspecified'))
        except Exception as exc:
            record=dict(status='failed',input_sha=sha256(source),config_sha=canonical_hash(config),error=f'{type(exc).__name__}: {exc}')
        manifest[source.name]=record;atomic_json(mp,manifest);emitted.append((source.name,record['status']))
    return emitted


def compare_regression(reference,current,allowed_ratio=1.30):
    # >>> X10
    # 요구: benchmark scope·device·imgsz·batch·model_sha가 같아야 시간 비교 가능.
    # 다르거나 필수 비교 키가 없으면 comparable=False와 원인 목록 반환.
    # 시간은 중앙값 ms이며 시간·허용 비율 모두 유한한 양수여야 한다(NaN/inf 금지).
    # 동일 조건에서 current/reference <= allowed_ratio이면 passed=True.
    # 시간 회귀만 판정하며 탐지 품질을 대신하지 않는다. CPU와 GPU를 섞지 않는다.
    raise NotImplementedError("TODO X10를 구현하세요.")
    # <<< X10
