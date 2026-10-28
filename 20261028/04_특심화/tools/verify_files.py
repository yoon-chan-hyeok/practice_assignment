"""배포 원본 파일의 SHA-256을 확인합니다. 학습자가 소스를 수정한 뒤에는 불일치가 정상입니다."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
    manifest=ROOT/'MANIFEST.sha256'
    errors=[];count=0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1);path=ROOT/name
        count+=1
        if not path.is_file():errors.append('누락: '+name)
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=digest:errors.append('변경: '+name)
    print(f'원본 무결성: {count}개 파일 / 불일치 {len(errors)}개')
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print('학습용 소스 수정 후에는 불일치가 정상입니다. 외부 파일의 안전성을 보증하는 검사는 아닙니다.')
if __name__=='__main__':main()
