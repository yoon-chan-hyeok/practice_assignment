"""실제 Hugging Face Tokenizer를 사용하는 선택 실습 (기본 과제와 독립).

최초 모델 다운로드는 네트워크·저장 공간이 필요합니다.
아무 옵션 없이 실행하면 로컬 캐시만 사용하여 인터넷을 자동으로 호출하지 않습니다.
"""
import argparse
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allow-download',action='store_true',help='캐시가 없을 때 Hugging Face 다운로드 허용')
    args=parser.parse_args()
    try:
        from transformers import AutoTokenizer
    except ImportError:
        print('선택 설치: python -m pip install transformers')
        return
    try:
        tokenizer=AutoTokenizer.from_pretrained('bert-base-multilingual-cased',
                                                local_files_only=not args.allow_download)
    except Exception as e:
        print('Tokenizer 파일을 사용할 수 없습니다:',type(e).__name__)
        print('사전 캐시가 없는 경우 --allow-download 옵션과 인터넷 연결이 필요합니다.')
        return
    for text in ['실습 파일은 개인 폴더에 보관합니다.','FastAPI와 PostgreSQL']:
        ids=tokenizer(text)['input_ids']
        print('TEXT:',text)
        print('TOKENS:',tokenizer.convert_ids_to_tokens(ids))
        print('INPUT_IDS:',ids,'LEN:',len(ids))
    pair=tokenizer(['AI','FastAPI와 PostgreSQL'],padding=True,truncation=True,
                   max_length=12,return_tensors='pt')
    print('BATCH:',tuple(pair['input_ids'].shape),'MASK:',pair['attention_mask'].tolist())
    print('교육용 ToyTokenizer 결과와 다릅니다. 특수 Token 규칙도 모델을 확인하세요.')

if __name__=='__main__':
    main()
