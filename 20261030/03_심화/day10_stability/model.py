"""제공 코드: 선택한 안정화 기법만 구조에 추가합니다."""
from torch import nn

def build_model(config):
    w = config["width"]
    layers = [nn.Linear(2, w)]
    if config["bn"]:
        layers.append(nn.BatchNorm1d(w))
    layers.extend([nn.ReLU(), nn.Dropout(config["dropout"]), nn.Linear(w, w)])
    if config["bn"]:
        layers.append(nn.BatchNorm1d(w))
    layers.extend([nn.ReLU(), nn.Dropout(config["dropout"]), nn.Linear(w, 2)])
    return nn.Sequential(*layers)
