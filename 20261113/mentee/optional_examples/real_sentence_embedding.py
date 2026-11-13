"""실제 문장 임베딩의 선택 시연. 기본필수 채점과 무관합니다."""
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allow-download',action='store_true')
    args=parser.parse_args()
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print('선택 설치: python -m pip install sentence-transformers')
        return
    model_name='sentence-transformers/all-MiniLM-L6-v2'
    try:
        model=SentenceTransformer(model_name,device='cpu',
                                  local_files_only=not args.allow_download)
    except Exception as e:
        print('모델 가중치를 사용할 수 없습니다:',type(e).__name__)
        print('--allow-download 옵션은 사용자가 다운로드를 허용할 때만 선택합니다.')
        return
    texts=['The file is in your project folder.',
           'Look for it in the project directory.',
           'The weather is sunny today.']
    vectors=model.encode(texts)
    print('shape:',vectors.shape)
    print('cosine similarity:',model.similarity(vectors,vectors))
    print('영어 예제의 결과를 한국어 성능으로 일반화하지 않습니다.')

if __name__=='__main__':
    main()
