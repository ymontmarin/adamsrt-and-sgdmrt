from os.path import expanduser

import torch
from torch.utils.data import DataLoader, Subset
from torchvision.datasets import CIFAR100
import torchvision.transforms as v_transforms


# CIFAR Mean and Std
MEAN = [0.5071, 0.4867, 0.4408]
STD = [0.2675, 0.2565, 0.2761]


def get_dataloader_cifar100(
    valid_split=0.05,
    train_batch_size=128,
    test_batch_size=128,
    dataset_root_path="/tmp/CIFAR100",
    num_workers=1
):
    '''
    Function that build the CIFAR dataloader with classic transform
    Return a train_loader and valid_loader which are a random split of the
    train dataset according valid_split
    Canonical data augmentation is apply on the train_loader
    Normalization is done for for all loader
    The valid loader use the test_batch_size

    Arguments:
        valid_split (float): percentage to cut off from train dataset for
            valid loader
        train_batch_size (int): size of batch to use for train_loader
        test_batch_size (int): size to use for test_loader, valid_loader
        num_workers (int): nuber of worker to use
    '''
    dataset_root_path = expanduser(dataset_root_path)
    # Build regular data transformation
    train_transforms = v_transforms.Compose([
        v_transforms.RandomCrop(32, padding=4),
        v_transforms.RandomHorizontalFlip(),
        v_transforms.ToTensor(),
        v_transforms.Normalize(mean=MEAN, std=STD),
    ])

    test_transforms = v_transforms.Compose([
        v_transforms.ToTensor(),
        v_transforms.Normalize(mean=MEAN, std=STD),
    ])

    train_dataset = CIFAR100(
        dataset_root_path,
        train=True,
        transform=train_transforms,
        download=True
    )
    test_dataset = CIFAR100(
        dataset_root_path,
        train=False,
        transform=test_transforms,
    )
    # Cut a part of train for valid
    n = len(train_dataset)
    # has been seeded with sacred special value _seed
    indices = torch.randperm(n)
    n_cut = n - int(valid_split * n)
    valid_dataset = Subset(train_dataset, indices[n_cut:])
    train_dataset = Subset(train_dataset, indices[:n_cut])

    data_loader_train = DataLoader(
        train_dataset,
        batch_size=train_batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    data_loader_valid = DataLoader(
        valid_dataset,
        batch_size=test_batch_size,
        num_workers=num_workers,
        pin_memory=True
    )
    data_loader_test = DataLoader(
        test_dataset,
        batch_size=test_batch_size,
        num_workers=num_workers,
        pin_memory=True
    )
    return data_loader_train, data_loader_valid, data_loader_test
