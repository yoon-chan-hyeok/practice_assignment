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

    # TODO D20-04-B01: Token ID 텐서와 nn.Embedding 출력의 shape (B,T,D)를 구하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-B01
    embedding = nn.Embedding(num_embeddings=16, embedding_dim=8)  # ID 16종, 특성 8개
    x = None       # TODO: embedding(token_ids) 호출
    id_shape = []  # TODO: token_ids.shape을 리스트로 변환
    emb_shape = [] # TODO: x.shape을 리스트로 변환
    raise NotImplementedError("D20-04-B01: TODO를 완성하세요")
    # END D20-04-B01

    # TODO D20-04-B02: EncoderLayer(d_model=8,nhead=2)로 전달하고 shape 보존을 검증하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-B02
    layer = nn.TransformerEncoderLayer(
        d_model=8, nhead=2, dim_feedforward=16, batch_first=True, dropout=0.0
    )
    layer.eval()
    pad_mask = token_ids == 0  # PAD 위치는 True로 표시
    y = None  # TODO: torch.no_grad() 안에서 layer(x, src_key_padding_mask=pad_mask)
    out_shape = []  # TODO: y.shape을 리스트로 변환
    # TODO: assert로 Embedding 입력/Encoder 출력 shape가 같은지 비교
    raise NotImplementedError("D20-04-B02: TODO를 완성하세요")
    # END D20-04-B02
    components={"attention":"토큰 간 정보","ffn":"특징 변환","shape":out_shape}
    padding_positions=[]
    pad_values=None
    padding_note="PAD Mask는 Causal Mask와 별개"
    head_divisibility_error=None
    extra_shapes={}
    architecture_note="이 코드는 Encoder Layer의 Shape 실습"

    # TODO D20-04-B03: 모든 shape와 Mask 의미를 transformer_report.json에 정리하세요.
    # 입력·대상: 예시 Token IDs는 batch=2, length=5입니다.
    # 완료 확인: outputs/transformer_report.json의 입력·출력 shape가 (2,5,8)인지 확인합니다.
    # 주의: EncoderLayer를 Decoder 기반 LLM 완성본과 혼동하지 않습니다.
    # BEGIN D20-04-B03
    report = {
        "ids": [],             # TODO: id_shape
        "embedding": [],       # TODO: emb_shape
        "encoder_output": [],  # TODO: out_shape
        "pad_key_mask": [],    # TODO: pad_mask.tolist()
        "components": components,
        "padding_positions": padding_positions,
        "padding_output_abs_sum": pad_values,
        "padding_note": padding_note,
        "bad_head_rejected": head_divisibility_error,
        "extra_shapes": extra_shapes,
        "architecture_note": architecture_note,
    }
    write_json(HERE / "outputs" / "transformer_report.json", report)
    raise NotImplementedError("D20-04-B03: TODO를 완성하세요")
    # END D20-04-B03

if __name__=="__main__":
    main()
