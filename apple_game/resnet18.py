from torchvision import models
from torch import nn, cuda
import torch
from PIL import Image
import numpy as np

device = "cuda" if cuda.is_available() else "cpu"
model = models.resnet18(pretrained=True)
model.conv1 = nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
model.fc = nn.Linear(model.fc.in_features, 9)
model.to(device)

best_checkpoint = torch.load("weight.pth",  map_location=device)
model.load_state_dict(best_checkpoint)

model.to(device)
model.eval()
X = Image.open("./data/test/1/1_6.png")
X = torch.from_numpy(np.asarray(X).reshape(1, 1, 28, 28)).float()
with torch.no_grad():
        X = X.to(device)
        outputs = model(X)
        _, preds = torch.max(outputs, 1)

#label은 정답 글자 - 1로 저장했었음
print(preds+1)