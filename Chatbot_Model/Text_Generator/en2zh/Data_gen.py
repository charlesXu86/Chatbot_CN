# encoding=utf-8
import itertools

import numpy as np
from torch.utils.data import Dataset

from Config import *

samples_path = 'data/samples_train.json'
samples = json.load(open(samples_path, 'r'))


# np.random.shuffle(samples)


def zeroPadding(l, fillvalue=PAD_token):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))


def binaryMatrix(l):
    m = []
    for i, seq in enumerate(l):
        m.append([])
        for token in seq:
            if token == PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    return m


# Returns padded input sequence tensor and lengths
def inputVar(indexes_batch):
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    padVar = torch.LongTensor(padList)
    return padVar, lengths


# Returns padded target sequence tensor, padding mask, and max target length
def outputVar(indexes_batch):
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    mask = binaryMatrix(padList)
    mask = torch.ByteTensor(mask)
    padVar = torch.LongTensor(padList)
    return padVar, mask, max_target_len


# Returns all items for a given batch of pairs
def batch2TrainData(pair_batch):
    pair_batch.sort(key=lambda x: len(x[0]), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
    inp, lengths = inputVar(input_batch)
    output, mask, max_target_len = outputVar(output_batch)
    return inp, lengths, output, mask, max_target_len


class TranslationDataset(Dataset):
    def __init__(self, split):
        self.split = split
        assert self.split in {'train', 'valid'}

        print('loading {} samples'.format(split))
        train_count = int(len(samples) * train_split)

        if split == 'train':
            self.samples = samples[:train_count]
        else:
            self.samples = samples[train_count:]

        self.num_chunks = len(self.samples) // chunk_size
        np.random.shuffle(self.samples)

        print('count: ' + str(len(self.samples)))

    def __getitem__(self, i):
        start_idx = i * chunk_size
        pair_batch = []

        for i_batch in range(chunk_size):
            sample = self.samples[start_idx + i_batch]
            pair_batch.append((sample['input'], sample['output']))

        return batch2TrainData(pair_batch)

    def __len__(self):
        return self.num_chunks


if __name__ == '__main__':
    print('loading {} samples'.format('train'))
    samples_path = 'data/samples_train.json'
    samples = json.load(open(samples_path, 'r'))
    pair_batch = []
    for i in range(5):
        sample = samples[i]
        pair_batch.append((sample['input'], sample['output']))

    # Example for validation
    small_batch_size = 5
    batches = batch2TrainData(pair_batch)
    input_variable, lengths, target_variable, mask, max_target_len = batches

    print("input_variable:", input_variable)
    print("lengths:", lengths)
    print("target_variable:", target_variable)
    print("mask:", mask)
    print("max_target_len:", max_target_len)
