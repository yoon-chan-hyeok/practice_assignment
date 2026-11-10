"""실제 로컬 VLM 선택 경로. transformers·모델 준비가 필요하며 제작 시 미검증입니다."""
from pathlib import Path
import argparse
from harness import run_documents
p=argparse.ArgumentParser();p.add_argument('--model-dir',required=True)
a=p.parse_args();base=Path(__file__).resolve().parent
counts=run_documents(base/'data',base/'outputs_real',{'backend':'real','model_dir':str(Path(a.model_dir).resolve()),'min_confidence':80.0,'schema_version':'invoice-v1'})
print(counts)
if counts['failed']:raise SystemExit('실패 문서가 있습니다. manifest의 error_type을 확인하세요. mock 대체 없음.')
