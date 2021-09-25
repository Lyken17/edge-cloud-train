
import time
import zmq
import io

import torch
import torch as th
import torch.nn as nn

from buffer import serialize, de_serialize
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

net = nn.Sequential(
    nn.Linear(5, 10),
    nn.Linear(10, 15),
    nn.Linear(15, 30),
)

print("Initialization finished")
while True:
    #  Wait for next request from client
    message = socket.recv()
    info = th.load(io.BytesIO(message))
    if info['flag'] == 0:
        input_data = info['data']
        print("[begin] Received request: ", input_data.shape)
        out = net(input_data)
        socket.send(serialize(out))
        print("[begin] Send output: ",  out.shape)
    elif info['flag'] == 1:
        grad_outputs = info['data']
        print("[end] Received grad_output: ", grad_outputs)
        grad_i = th.autograd.grad(out, input_data, grad_outputs=grad_outputs)[0]
        print("[end] Send dy/dx: ", grad_i.shape)
        socket.send(serialize(grad_i))
    elif info['flag'] == -1:
        socket.send(b'finish')
        break
    time.sleep(1)
