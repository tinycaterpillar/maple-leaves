from torchvision import models

model = models.resnet18(pretrained=True)
model.conv1 = nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
model.fc = nn.Linear(model.fc.in_features, 9)
model.eval()

outputs = model(inputs)
_, preds = torch.max(outputs, 1)
print(preds