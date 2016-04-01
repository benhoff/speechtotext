import sys
import atexit
import time

from os import path
from subprocess import Popen

import zmq


directory = path.dirname(__file__)
src_dir = path.realpath(path.join(directory, '..', 'speechtotext'))
main_filepath = path.join(src_dir,
                          '__main__.py')

process = Popen((sys.executable,
                 main_filepath,
                 '--audio_address',
                 'tcp://127.0.0.1:5655'))
time.sleep(1)

def _kill_process(process):
    def actually_kills_process():
        process.kill()
    return actually_kills_process

atexit.register(_kill_process(process))

context = zmq.Context()
communication_socket = context.socket(zmq.REQ)
# FIXME: inconsistent default args in microphone
communication_socket.connect('tcp://127.0.0.1:5561')
audio_socket = context.socket(zmq.SUB)
audio_socket.setsockopt(zmq.SUBSCRIBE, b'')

while True:
    # first thing we want is a driver socket ID.
    command_type = b'metadriver'
    command = b'list_drivers'
    frame = (command_type, command, b'')

    print('sending driver request')
    communication_socket.send_multipart(frame)
    print('sent')
    response = communication_socket.recv_multipart()
    print('got response', response)
    driver_socket_id = response[0]
    print(driver_socket_id)

    command_type = b'driver'
    command = b'record'

    frame = (command_type, command, driver_socket_id)

    print('send record command!')
    communication_socket.send_multipart(frame)
    print('sent record command')
    # NOTE: this should block right here
    reply = communication_socket.recv_multipart()
    print(reply)
