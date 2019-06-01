#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    socket_server_test 
Author:   Liuyl 
DateTime: 2014/12/11 10:42 
UpdateLog:
1、Liuyl 2014/12/11 Create this File.

socket_server_test
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
import SocketServer


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # just send back the same dataDict, but upper-cased
        self.request.send(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "192.168.1.30", 8077

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()