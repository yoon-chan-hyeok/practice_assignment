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

def run_analysis():
    token_ids=torch.tensor([[2,4,5,3,0],[2,6,7,3,0]],dtype=torch.long)

    # TODO D20-04-A01: Token ID 텐서와 nn.Embedding 출력의 shape (B,T,D)를 구하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A01
    raise NotImplementedError("D20-04-A01: TODO를 완성하세요")
    # END D20-04-A01

    # TODO D20-04-A02: EncoderLayer(d_model=8,nhead=2)로 전달하고 shape 보존을 검증하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A02
    raise NotImplementedError("D20-04-A02: TODO를 완성하세요")
    # END D20-04-A02

    # TODO D20-04-A03: Residual·LayerNorm·FFN이 바꾸는 값과 보존하는 shape를 기록하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A03
    raise NotImplementedError("D20-04-A03: TODO를 완성하세요")
    # END D20-04-A03

    # TODO D20-04-A04: Padding 위치가 attention의 Key/Value에서 제외되지만 출력 위치가 자동 0이 아님을 확인하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A04
    raise NotImplementedError("D20-04-A04: TODO를 완성하세요")
    # END D20-04-A04

    # TODO D20-04-A05: d_model=8에서 nhead=3은 나눠지지 않아 실패함을 안전하게 검사하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A05
    raise NotImplementedError("D20-04-A05: TODO를 완성하세요")
    # END D20-04-A05

    # TODO D20-04-A06: 입력 shape가 다른 테스트와 encoder/decoder의 마스크 차이를 기록하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A06
    raise NotImplementedError("D20-04-A06: TODO를 완성하세요")
    # END D20-04-A06

    # TODO D20-04-A07: 모든 shape와 Mask 의미를 transformer_report.json에 정리하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-A07
    raise NotImplementedError("D20-04-A07: TODO를 완성하세요")
    # END D20-04-A07

