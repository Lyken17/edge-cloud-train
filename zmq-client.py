import zmq
import io
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

import torch as th

from buffer import serialize, de_serialize

for request in range(10):
    print("Sending request %s …" % request)
    
    b = th.ones(1) * request
    # socket.send(serialize(b))
    buffer = io.BytesIO()
    th.save({
        "flag": 1,
        "data": b
    }, buffer)

    socket.send(buffer.getvalue())
    message = socket.recv()

    # message = socket.recv()
    # print("Received reply %s" % (request, ), de_serialize(message))
    
    # socket.send(b"Hello")
    # message = socket.recv()
    # print("Received reply %s [ %s ]" % (request, message))
