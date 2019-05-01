'''
Student Name: Matthew Carroll
Date: May 1, 2019

Program Description:
This is the Client Side of the Program. It creates a socket and connects
using the host and port global variables. Then, after a connection is established
it loops continuously prompting the user for inputs and sends them to the server.
The server (described more on the server.py file) processes them and sends a response
printed to the client. Once logout is entered, the connection is closed and the client.py
script terminates.

'''


import sys
import socket
import time

#global variables
host = '127.0.0.1'
port = 12619

if __name__ == '__main__':
    #make socket and connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('My Chat Room Client V1')
    try:
        #loop and continuously accept new messages from client
        while True:
            message = input('>')
            #send the message over the socket
            sock.send(message.encode())
            #just do this so it gives time for the server to process. Don't want Windows doing anything weird
            time.sleep(1)
            #recieve the message over the socket
            ret_message = sock.recv(1024)
            #decode from bytes to string
            ret_message = ret_message.decode()
            print(ret_message)
            #if I tried to logout, lets logout
            if ret_message == '>Server: Connection closed':
                break
    #yay, sys.stdin doesn't block the main thread on Windows so this is kinda pointless,
    #but it's nice on Unix OSes. Also it's just left over from when I started with V2
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
   

