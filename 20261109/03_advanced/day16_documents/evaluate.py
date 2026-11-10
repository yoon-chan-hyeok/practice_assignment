"""평가 도구: 추출 함수와 분리하여 정답이 추론 경로에 들어가지 않도록 합니다."""
import unicodedata

def normalize(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())

def edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(current[-1]+1, previous[j]+1, previous[j-1]+(ca!=cb)))
        previous = current
    return previous[-1]

def cer(reference, predicted):
    """NFC·연속 공백 정규화 후 CER. 빈 정답에 삽입만 있으면 None(정의 불가)."""
    a,b = normalize(reference),normalize(predicted)
    if not a:
        return 0.0 if not b else None
    return edit_distance(a,b)/len(a)  # 삽입이 많으면 1보다 클 수 있습니다.

def field_scores(predictions, truth):
    rows=[]
    for name in ('issued_at','supplier','total_amount'):
        pred=predictions[name]['value']
        rows.append({'field':name,'predicted':pred,'reference':truth[name],'exact':type(pred) is type(truth[name]) and pred==truth[name]})
    return rows
