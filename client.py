import sys
import socket
import selectors
import types

host = '127.0.0.1'
port = 12619
connid = ''
sel = selectors.DefaultSelector()
messages = [b'Message 1 from client.', b'Message 2 from client.']

#starts the connection between the client and server
#needs the message to send, the connection id, 
def start_connections(host, port):
    server_addr = (host, port)
    for i in range(0, 1):
        #connid is how we can identify each connection
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid, 
                                    msg_total=sum(len(m) for m in messages), 
                                    recv_total=0, 
                                    messages=list(messages), 
                                    outb = b'')
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('recieved', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]



start_connections(host, port)

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()

#takes in the info string and changes the connid accordingly    
# def login(info):


#takes in the info string and sends the info to the server using start_connections
# def send(info):


# def newuser(info):


#returns connid
# def who(info):



# if __name__ == "__main__":
#     print("My chat room client. Version Two\n")
    
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, port))
#         s.sendall(b'Hello, world')
#         data = s.recv(1024)

#     print('Received', repr(data))
    
#     choice = raw_input("")
#     c_input = choice.split()
#     while c_input[0] != 'logout':
#         if c_input[0] == 'login':
#             login(c_input)
#         elif c_input[0] == 'send':
#             send(c_input)
#         elif c_input[0] == 'newuser':
#             newuser(c_input)
#         elif c_input[0] == 'who':
#             who(c_input)
#         elif c_input[0] == 'logout':
#             break
#         else:
#             print('Invalid command\n')


