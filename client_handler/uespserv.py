"""
Socket thread for client-server communications
"""

import _thread
import socket
import time
from client_handler import debugger
from config import constants


class ComsThread:
    def __init__(self, sen, ip, dbg: debugger.Debug):
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a streaming socket
        serversock.bind((ip, constants.SOCKET_PORT))  # bind the socket on given local ip and port
        serversock.listen(5)
        print("Socket initialized")

        def handle(serversocket, sensors, debug: debugger.Debug):
            (clientsocket, address) = serversocket.accept()  # wait for a client to connect
            while 1:
                try:
                    data = clientsocket.recv(1024)  # client sent data
                    if not data:  # data is empty, client is gone
                        break
                    lt = time.localtime()
                    date = "{:02d}/{:02d}".format(lt[2], lt[1])
                    tijd = "{:02d}:{:02d}:{:02d}".format(lt[3], lt[4], lt[5])
                    if data == b"rbt":
                        clientsocket.send(b"rebooting now")
                        clientsocket.close()
                        import machine
                        machine.reset()
                    elif data == b"dbg":  # client asked for a debug
                        clientsocket.send((date + " " + tijd + " " + str(debug)).encode())
                        break  # break further connection with the client en expect a new one
                    else:  # just send the client sensor readings
                        clientsocket.send((date + " " + tijd + " " + str(sensors)).encode())
                except Exception as e:
                    print(e)
                    break  # something went wrong, bail!
            handle(serversocket, sensors, debug)  # looks like the client is gone, prepare for a new one

        _thread.start_new_thread(handle, (serversock, sen, dbg))  # do the handle stuff above in a thread
