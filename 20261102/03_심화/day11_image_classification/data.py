"""입력 폴더와 변환을 구성한다. 원본 split을 바꾸거나 test를 읽지 않는다."""
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import ResNet18_Weights

ROOT = Path(__file__).resolve().parent

def load_data(kind="small", augment=False, batch_size=16, seed=42):
    """반환: train_aug, train_eval, valid, train_loader, train_eval_loader, valid_loader."""
    if kind == "small":
        evaluation = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
        training = transforms.Compose([transforms.Resize((32, 32)), transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(10), transforms.ToTensor()]) if augment else evaluation
    else:
        # 사전학습 weight의 공식 전처리는 224×224와 지정 Normalize를 포함한다.
        evaluation = ResNet18_Weights.IMAGENET1K_V1.transforms()
        training = evaluation
    train = datasets.ImageFolder(ROOT / "data" / "train", transform=training)
    train_eval = datasets.ImageFolder(ROOT / "data" / "train", transform=evaluation)
    valid = datasets.ImageFolder(ROOT / "data" / "valid", transform=evaluation)
    generator = torch.Generator().manual_seed(seed)
    loaders = (DataLoader(train, batch_size=batch_size, shuffle=True, generator=generator, num_workers=0),
               DataLoader(train_eval, batch_size=batch_size, shuffle=False, num_workers=0),
               DataLoader(valid, batch_size=batch_size, shuffle=False, num_workers=0))
    return train, train_eval, valid, *loaders
