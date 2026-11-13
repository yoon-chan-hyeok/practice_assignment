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

    # BEGIN D20-04-B01
    embedding=nn.Embedding(num_embeddings=16,embedding_dim=8)
    x=embedding(token_ids)
    id_shape=list(token_ids.shape)
    emb_shape=list(x.shape)
    # 해설: 정수 ID shape (2,5)에서 실수 Token Vector shape (2,5,8)로 변화합니다.
    # END D20-04-B01

    # BEGIN D20-04-B02
    layer=nn.TransformerEncoderLayer(d_model=8,nhead=2,dim_feedforward=16,
                                     batch_first=True,dropout=0.0)
    layer.eval()
    pad_mask=(token_ids==0)  # MultiheadAttention의 padding mask에서 True는 차단입니다.
    with torch.no_grad():
        y=layer(x,src_key_padding_mask=pad_mask)
    assert x.shape==y.shape
    out_shape=list(y.shape)
    # 해설: Encoder 출력 차원 보존은 LM Head의 어휘 Logit 생성과 별개입니다.
    # END D20-04-B02
    components={"attention":"토큰 간 정보","ffn":"특징 변환","shape":out_shape}
    padding_positions=[]
    pad_values=None
    padding_note="PAD Mask는 Causal Mask와 별개"
    head_divisibility_error=None
    extra_shapes={}
    architecture_note="이 코드는 Encoder Layer의 Shape 실습"

    # BEGIN D20-04-B03
    write_json(HERE/"outputs"/"transformer_report.json",{
        "ids":id_shape,"embedding":emb_shape,"encoder_output":out_shape,
        "pad_key_mask":pad_mask.tolist(),"padding_positions":padding_positions,
        "padding_output_abs_sum":pad_values,"padding_note":padding_note,
        "components":components,"bad_head_rejected":head_divisibility_error,
        "extra_shapes":extra_shapes,"architecture_note":architecture_note,
    })
    print("[04]",id_shape,"=>",emb_shape,"=>",out_shape)
    # END D20-04-B03

if __name__=="__main__":
    main()
