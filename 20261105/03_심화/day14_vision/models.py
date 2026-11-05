"""소형 source Backbone과 Head. ImageNet/ResNet18 결과로 표기하지 않습니다."""
from pathlib import Path
import numpy as np
import torch
from torch import nn


def build_model(data: Path, pretrained: bool = True, seed: int = 14) -> nn.Sequential:
    """제공된 source 표현을 재사용하고 새 Head는 같은 seed로 초기화합니다."""
    torch.manual_seed(seed)
    model = nn.Sequential(
        nn.Conv2d(3,8,3,padding=1,bias=False), nn.BatchNorm2d(8), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8,16,3,padding=1,bias=False), nn.BatchNorm2d(16), nn.ReLU(),
        nn.AdaptiveAvgPool2d((4,4)), nn.Flatten(), nn.Linear(256,3),
    )
    if pretrained:
        with np.load(Path(data)/'source_backbone.npz', allow_pickle=False) as saved:
            state=model.state_dict()
            state.update({key:torch.from_numpy(saved[key].copy()) for key in saved.files})
        model.load_state_dict(state)
    return model


def configure(model, strategy='head', head_lr=.01, backbone_lr=.001):
    """Head / 마지막 Conv+Head / 전체. Parameter 그룹을 겹치지 않게 만듭니다."""
    if strategy not in {'head','partial','full'}:
        raise ValueError('strategy must be head, partial, or full')
    for p in model.parameters():p.requires_grad_(False)
    for p in model[9].parameters():p.requires_grad_(True)
    groups=[{'params':list(model[9].parameters()), 'lr':head_lr}]
    if strategy != 'head':
        backbone=list(model[4:6].parameters()) if strategy=='partial' else list(model[:9].parameters())
        for p in backbone:p.requires_grad_(True)
        groups.append({'params':backbone,'lr':backbone_lr})
    return torch.optim.AdamW(groups,weight_decay=.0001)


def training_mode(model, freeze_bn=True):
    """eval은 autograd를 끄지 않습니다. BN 통계와 affine gradient는 별도 정책입니다."""
    model.train()
    if freeze_bn:
        for layer in model.modules():
            if isinstance(layer,nn.modules.batchnorm._BatchNorm):layer.eval()
