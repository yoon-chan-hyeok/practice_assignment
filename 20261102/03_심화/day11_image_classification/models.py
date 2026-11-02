"""작은 CNN과 실제 사전학습 모델을 구성한다. 원리 설명용 클래스는 제공 코드다."""
from torch import nn
from torchvision.models import resnet18, ResNet18_Weights

class SmallCNN(nn.Module):
    def __init__(self, width=16, batchnorm=False, dropout=0.0):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, width, 3, padding=1),
            nn.BatchNorm2d(width) if batchnorm else nn.Identity(), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(width, width*2, 3, padding=1),
            nn.BatchNorm2d(width*2) if batchnorm else nn.Identity(), nn.ReLU(), nn.MaxPool2d(2),
            nn.Dropout2d(dropout), nn.AdaptiveAvgPool2d(1), nn.Flatten(),
        )
        self.fc = nn.Linear(width*2, 2)

    def forward(self, x):
        return self.fc(self.features(x))

def build_model(kind="small", width=16, batchnorm=False, dropout=0.0, pretrained=True):
    """pretrained=False는 QA 구조 점검 전용. 학습 비교표에서는 사용하지 않는다."""
    if kind == "small":
        return SmallCNN(width, batchnorm, dropout)
    weights = ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = resnet18(weights=weights)
    for parameter in model.parameters():
        parameter.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, 2)
    if kind == "partial":
        for parameter in model.layer4.parameters():
            parameter.requires_grad = True
    return model

def set_training_mode(model, kind):
    """Backbone 고정에는 gradient뿐 아니라 BatchNorm 버퍼 정책도 필요하다."""
    if kind == "small":
        model.train()
    else:
        model.eval()
        model.fc.train()
        if kind == "partial":
            model.layer4.train()
            for layer in model.layer4.modules():
                if isinstance(layer, nn.BatchNorm2d):
                    layer.eval()  # 작은 학습표본에서는 BN running 통계를 보존한다.
