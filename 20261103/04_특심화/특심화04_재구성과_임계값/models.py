"""제공 모듈: 모델의 입력·출력 규칙만 정의한다. 실험·파일 저장은 하지 않는다."""
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

class RecurrentModel(nn.Module):
    """BTF 입력을 마지막 실제 상태로 요약한다. task는 regression 또는 classification."""
    def __init__(self, kind='LSTM', features=1, hidden=8, outputs=1, packed=True):
        super().__init__()
        self.kind, self.packed = kind, packed
        recurrent = nn.RNN if kind == 'RNN' else nn.LSTM
        self.core = recurrent(features, hidden, batch_first=True)
        self.head = nn.Linear(hidden, outputs)

    def forward(self, x, lengths=None):
        # 각 Sequence는 독립 표본이므로 앞 배치의 hidden을 이어받지 않는다.
        incoming = pack_padded_sequence(x, lengths.cpu(), batch_first=True,
                    enforce_sorted=False) if self.packed and lengths is not None else x
        _, state = self.core(incoming)
        h = state[0] if self.kind == 'LSTM' else state
        return self.head(h[-1])

class AttentionModel(nn.Module):
    """위치 임베딩과 Padding key mask, masked mean으로 분류한다."""
    def __init__(self, features=3, hidden=8, outputs=2, max_len=64, dropout=0.0):
        super().__init__()
        self.projection = nn.Linear(features, hidden)
        self.position = nn.Embedding(max_len, hidden)
        layer = nn.TransformerEncoderLayer(hidden, 2, dim_feedforward=16,
                    dropout=dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, 1, enable_nested_tensor=False)
        self.head = nn.Linear(hidden, outputs)

    def forward(self, x, lengths):
        positions = torch.arange(x.size(1), device=x.device)
        mask = positions.unsqueeze(0) >= lengths.to(x.device).unsqueeze(1)
        z = self.projection(x) + self.position(positions)
        z = self.encoder(z, src_key_padding_mask=mask)
        # key만 차단하면 padded query의 출력은 남을 수 있다. pooling에서도 제외한다.
        pooled = (z * (~mask).unsqueeze(-1)).sum(1) / lengths.to(x.device).unsqueeze(1)
        return self.head(pooled)

class Autoencoder(nn.Module):
    def __init__(self, features=8, latent=2):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(features, latent), nn.Tanh())
        self.decoder = nn.Linear(latent, features)

    def forward(self, x, lengths=None):
        return self.decoder(self.encoder(x))

def classifier(kind):
    # 파라미터 수를 완전히 같게 하지는 않는다. 대략 비슷한 범위로 맞추고 실제 수를 기록한다.
    if kind == 'Transformer':
        return AttentionModel()
    return RecurrentModel(kind, features=3, hidden=24 if kind=='RNN' else 12, outputs=2)
