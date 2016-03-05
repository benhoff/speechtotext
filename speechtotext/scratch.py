import sys
import atexit

from os import path
from subprocess import Popen

import zmq


directory = path.dirname(__file__)
main_filepath = path.join(directory,
                          '__main__.py')

process = Popen((sys.executable, main_filepath))

def _shutdown_method():
    process.kill()

atexit.register(_shutdown_method)

context = zmq.Context()
communication_socket = context.socket(zmq.REQ)
communication_socket.connect('tcp://127.0.0.1:5561')

while True:
    # first thing we want is a driver socket ID.
    command_type = b'metadriver'
    command = b'list_drivers'
    frame = (command_type, command, b'')

    communication_socket.send_multipart(frame)
    response = communication_socket.recv_multipart()
    driver_socket_id = response[0]

    command_type = b'driver'
    command = b'record'

    frame = (command_type, command, driver_socket_id)

    print('send record command!')
    communication_socket.send_multipart(frame)
    print('sent record command')
    # NOTE: this should block right here
    reply = communication_socket.recv_multipart()
    print(reply)
