"""실습 04 · 필요한 하위 폴더는 ImageFolder의 이미지 저장 구조뿐이다."""
from pathlib import Path
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

root = Path(__file__).resolve().parent
# Resize(size)는 목표 크기가 필수. ToTensor()에는 필수 인자가 없다.
transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
# ImageFolder(root, transform=None): root는 필수, transform은 선택이다.
# BEGIN B04
# TODO B04: data/train을 주어진 transform으로 읽는다.
train = datasets.ImageFolder(root / "data" / "train")
# END B04
loader = DataLoader(train, batch_size=4, shuffle=False, num_workers=0)
images, labels = next(iter(loader))
print("학습 이미지:", len(train))
print("클래스:", train.class_to_idx)
print("배치:", tuple(images.shape), tuple(labels.shape))
print("라벨:", labels.tolist())
