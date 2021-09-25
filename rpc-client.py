# On worker 0:
import os

import torch
import torch.nn as nn
import torch.distributed.rpc as rpc
import torch.multiprocessing as mp

os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '29500'

rank = 1
world_size = 2
rpc.init_rpc("client", rank=rank, world_size=world_size)
ret = rpc.rpc_sync("ps", torch.add, args=(torch.ones(1, 10, requires_grad=True), torch.ones(1, 10, requires_grad=True)))
rpc.shutdown()