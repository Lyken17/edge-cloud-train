
import time
import zmq
import io
import torch as th
import torch.nn as nn

from buffer import serialize, de_serialize
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

net = nn.Sequential(
    nn.Linear(10, 10),
)


while True:
    #  Wait for next request from client
    message = socket.recv()
    # t = de_serialize(message)
    buffer = io.BytesIO(message)
    info = th.load(buffer)
    print("Received request: ", info['flag'])

    time.sleep(1)
    socket.send(b"World")
    #  Do some 'work'
    # time.sleep(1)
    # out = net(t)

    #  Send reply back to client
    # socket.send(serialize(out))