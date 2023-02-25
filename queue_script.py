import os
import torch
from tqdm import tqdm
import time


def check_mem(cuda_device):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().strip().split(
        "\n")
    total, used = devices_info[cuda_device].split(',')
    return total, used


def occumpy_mem(cuda_device):
    total, used = check_mem(cuda_device)
    total = int(total)
    used = int(used)
    max_mem = int(total * 0.9)
    block_mem = max_mem - used
    # x = torch.cuda.FloatTensor(256, 1024, block_mem)
    print("total",total)
    print("used",used)
    x = torch.FloatTensor(256, 1024, block_mem).cuda(cuda_device)
    del x


if __name__ == '__main__':
    import argparse
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--device_ids', help='device_ids', type=int, nargs="+",
                        default=list(range(torch.cuda.device_count())))
    parser.add_argument('--time', help='occumpy time(s)', type=int, default=1000000)
    args = parser.parse_args()
    for cuda_device in args.device_ids:
        occumpy_mem(cuda_device)
    for _ in tqdm(range(args.time)):
        time.sleep(1)
    print('Done')