'''
Student Name: Matthew Carroll
Date: May 1, 2019

Program Description:
This is the Server Side of the Program. It does all of the heavy lifting of this project. 
It starts out by opening the users.txt file and reading all ids and passwords from it into 
a global dictionary to easily use. Then, it processes the messages send from the client. It
uses each command as its own function and splits them appropriately into login, newuser, logout, 
and send. Each does as specified in the lab and prints error messages to both server and client
standard out. When logout is entered, the server closes the socket connection to the current
client and loops back to find a new connection with a new client.

'''

import sys
import socket

#global variables because they make this script fairly easy
host = '127.0.0.1'
port = 12619
#security info yay
user_info = {}
login_status = False
login_name = ''
name = 'Server'

#validate user info on server
def login(message):
    val = ''
    #check that user is logged in and report
    if login_status is True:
        print('Already logged in!')
        return '>Server: Already logged in!'
    #error check for size of user input
    if len(message) != 3:
        print('Invalid attempt at login!')
        return '>Server: incorrect syntax. Correct syntax is: login [UserID] [Password]'
    provided_id = message[1]
    provided_pass = message[2]
    #if the userID provided exists...
    if provided_id in user_info.keys():
        #if the password matches the userID...
        if provided_pass == user_info[provided_id]:
            print('Successful login')
            change_login(provided_id)
            val = '>Server: ' + login_name + ' joins'
        else:
            print('Incorrect login')
            val = '>Server: Incorrect login'
    else:
        print('Incorrect login')
        val = '>Server: Incorrect login'
    return val

#helper function for logout and login, userID is what the client will be known as
def change_login(user_id):
    global login_status
    global login_name
    val = ''
    #fires if logging out
    if login_status == True:
        print('Connection closed')
        val = '>Server: Connection closed'
        login_status = False
    #fires if logging in
    else:
        login_status = True
    login_name = user_id
    return val   

#signal to close connection and flips global variables back to original positions
def logout(message):
    val = '>Server: Connection closed'
    if login_status is True:
        val = change_login('')
    return val

#standard send function, pull front command off and send back with userID
def send(message):
    #error check to login first
    if login_status is False:
        print('You must log in!')
        return '>Server: Denied. Please login first.'
    #im lazy and decided to flat out change the message instead of copying it
    message = ' '.join(message)
    message = message[4:]
    message = ('>' + login_name + ':' + message)
    print(message)
    return message

def newuser(message):
    #make sure only 3 commands were submitted
    if len(message) != 3:
        print('Invalid attempt at user creation!')
        return '>Server: incorrect syntax. Correct syntax is: newuser [UserID] [Password]'
    provided_id = message[1]
    provided_pass = message[2]
    #make sure the new userID doesn't already exist
    if provided_id in user_info.keys():
        print('Attempted to register already created user')
        return '>Server: Username already taken, please choose another or login to continue'
    #make sure the userID isn't too large
    if len(provided_id) >= 32:
        print('Invalid username length')
        return '>Server: Please create a username less than 32 characters'
    #oh dear god this is a bad password, brute force could crack this in minutes if not seconds   
    #but per requirements make sure it is the specific length 
    if len(provided_pass) < 4 or len(provided_pass) > 8:
        print('Invalid password length')
        return '>Server: Invalid password length'
    user_info[provided_id] = provided_pass
    #write the new info to the file
    f = open('users.txt', 'a')
    f.write('\n' + provided_id + ',' + provided_pass)
    f.close()
    if login_status == False:
        print('New User Created. Please login.')
        appended = 'Please login.'
    else:
        print('New User Created.')
        appended = ''
    return '>Server: New User Created.' + appended

#wrapper function that manages all others
def parse_message(message):
    vals = str(message).split(' ')
    command = vals[0]
    #this maps each of the commands to a function name so I can pass it easier
    function_calls = {
        'login' : login,
        'logout' : logout,
        'send' : send,
        'newuser' : newuser
    }
    #if the command exists
    if command in function_calls.keys():
        st = function_calls[command](vals)
    else:
        print('Invalid function call!')
        st = '>Server: Invalid command'
    return st


#general main function
if __name__ == '__main__':
    #open and read in file to dictionary containing user data
    #this is terrible security practice, but I don't care at the moment
    f = open('users.txt', 'r')
    for line in f:
        line = line.strip('\n')
        info = line.split(',')
        user_info[info[0]] = info[1]
    f.close()

    #here is the socket connection part, only loops 1 time per client connection
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        print('listening on', (host, port))
        print('Waiting for connection')
        connection, addr = sock.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        try:
            #this runs with every message sent, since the pattern is call and response
            #it was easier to just recv/send/recv/send over and over
            while True:
                message = connection.recv(1024)
                message = message.decode()
                ret_message = str(parse_message(message))
                #this is what is printed on the client side application
                connection.send(ret_message.encode())
                if ret_message == '>Server: Connection closed':
                    sock.close()
                    break
        #yay, sys.stdin doesn't block the main thread on Windows so this is kinda pointless,
        #but it's nice on Unix OSes. Also it's just left over from when I started with V2 
        except KeyboardInterrupt:
            print("Interrupted by user, exiting")
