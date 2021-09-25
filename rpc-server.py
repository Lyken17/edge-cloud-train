# On worker 0:
import os

import torch
import torch.nn as nn
import torch.distributed.rpc as rpc
import torch.multiprocessing as mp

os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '29500'

rank = 0
world_size = 2
rpc.init_rpc("ps", rank=rank, world_size=world_size)
print("waiting for tasks")
rpc.shutdown()