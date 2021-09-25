
import time
import zmq
import io

import torch
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from torch import autograd

import torch as th
from buffer import serialize, de_serialize

print("Connecting to hello world server…")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

class RemotePassBegin(autograd.Function):
    @staticmethod
    def forward(ctx, input):
        buffer = io.BytesIO()
        th.save({
            "flag": 0, # forward
            "data": input
        }, buffer)
        
        socket.send(buffer.getvalue())
        return input

    @staticmethod
    def backward(ctx, grad_output):
        # return grad_output
        return de_serialize(socket.recv())

class RemotePassEnd(autograd.Function):
    @staticmethod
    def forward(ctx, input):
        # ctx.input = input
        return de_serialize(socket.recv())

    @staticmethod
    def backward(ctx, grad_output):
        buffer = io.BytesIO()
        th.save({
            "flag": 1, # backward
            "data": grad_output
        }, buffer)
        
        socket.send(buffer.getvalue())
        return None

for request in range(10):
    b = th.ones(5, requires_grad=True) * request
    print("Sending request %s …" % request)
    x = b
    x = RemotePassBegin.apply(x)
    x = RemotePassEnd.apply(x)
    print("output shape:", x.shape)
    x.sum().backward()