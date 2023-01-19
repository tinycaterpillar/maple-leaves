import numpy as np
from glob import glob
from PIL import Image
from tqdm import tqdm

def neighbor_loss(label, example, dist):
    row, col = label.shape
    loss = 0
    for r in range(dist, row - dist):
        for c in range(dist, col - dist):
            sub_label = label[r-dist:r+dist+1, c-dist:c+dist+1]
            loss += np.min(np.abs(example[r, c]-sub_label))**2
    return loss

def loss(labels, examples, dist):
    loss = [[0]*10 for _ in range(10)]
    for l_idx, l_data in tqdm(enumerate(test_data[1:], start = 1)):
        for t_idx, t_data in enumerate(train_data[1:], start = 1):
            loss[l_idx][t_idx] = sum(map(lambda i: neighbor_loss(l_data[0], i, dist), t_data)) // len(t_data)
    return loss

train_path = "./data/train/*"
train_data = [[] for _ in range(10)]
for i in glob(train_path):
    for j in glob(i+'/*'):
        im = Image.open(j)
        im = im.convert('L')
        im = im.resize((28, 28))
        im = np.asarray(im)
        train_data[int(i[-1])].append(im)

test_path = "./data/test/*"
test_data = [[] for _ in range(10)]
for i in glob(test_path):
    for j in glob(i+'/*'):
        im = Image.open(j)
        im = im.convert('L')
        im = im.resize((28, 28))
        im = np.asarray(im)
        test_data[int(i[-1])].append(im)

ans = loss(test_data, train_data, 5)
for i in ans[1:]: print(*i[1:],"->", i[1:].index(min(i[1:]))+1)