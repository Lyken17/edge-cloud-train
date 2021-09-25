import zmq
import io
import torch as th

def serialize(pth_tensor):
    buffer = io.BytesIO()
    th.save(pth_tensor, buffer)
    return buffer.getvalue()

def de_serialize(bin_buffer):
    nb = io.BytesIO(bin_buffer)
    return th.load( nb)
