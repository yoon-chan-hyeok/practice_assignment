from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
import torch
from torch import nn
from common.support import write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def main():
    token_ids=torch.tensor([[2,4,5,3,0],[2,6,7,3,0]],dtype=torch.long)

    # TODO D20-04-I01: Token ID 텐서와 nn.Embedding 출력의 shape (B,T,D)를 구하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-I01
    raise NotImplementedError("D20-04-I01: TODO를 완성하세요")
    # END D20-04-I01

    # TODO D20-04-I02: EncoderLayer(d_model=8,nhead=2)로 전달하고 shape 보존을 검증하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-I02
    raise NotImplementedError("D20-04-I02: TODO를 완성하세요")
    # END D20-04-I02

    # TODO D20-04-I03: Residual·LayerNorm·FFN이 바꾸는 값과 보존하는 shape를 기록하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-I03
    raise NotImplementedError("D20-04-I03: TODO를 완성하세요")
    # END D20-04-I03

    # TODO D20-04-I04: Padding 위치가 attention의 Key/Value에서 제외되지만 출력 위치가 자동 0이 아님을 확인하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-I04
    raise NotImplementedError("D20-04-I04: TODO를 완성하세요")
    # END D20-04-I04
    head_divisibility_error=None
    extra_shapes={}
    architecture_note="이 코드는 Encoder Layer의 Shape 실습"

    # TODO D20-04-I05: 모든 shape와 Mask 의미를 transformer_report.json에 정리하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-I05
    raise NotImplementedError("D20-04-I05: TODO를 완성하세요")
    # END D20-04-I05

if __name__=="__main__":
    main()
