import socket
import sys
import threading
from queue import Queue
import os

NO_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_addresses = []
rno = []

#create a socket allows to connect
all_clients = []
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999 # port tells us what data is actualy coming in
        s = socket.socket()
    except socket.error as msg:
        print ("Socket error"+str(msg))

# bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s

        print ("Binding!!!"+str(port))
        s.bind((host,port)) # a tuple as argument
        s.listen(5) # this allows our server to accept connection and 5 here is the number of try after which it will fail
                    # these are called bad connections
    except socket.error as msg:
        print ("Socket binding error!!!!\nRetrying!!!")
        #socket_bind()

# Establish a connection with client (socket must be listening)

def accept_connections():
    global host
    global port
    global s
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn , address = s.accept()
            conn.setblocking(1)
            roll = conn.recv(1024)
            if str(roll,"utf-8") in rno:
                conn.send(str.encode("Already connected to the server\nPlease wait for your turn.","utf-8"))
                conn.close()
            else:
                rno.append(str(roll,"utf-8"))
                all_connections.append(conn)
                all_addresses.append(address)
                print ("\nConnection established with: "+ address[0])
                conn.send(str.encode("You are now connected to the server\nPlease wait for your turn :)","utf-8"))
        except:
            print ("\nError accepting Connection")

# Custom Prompt
def prompt():
    while True:
        cmds = input("prompt:~$")
        if cmds == 'connections':
            list_connections()
            continue
        elif 'select ' in cmds:
            con = get_target(cmds)
            if con is not None:
                send_target_commands(con)
        elif 'exit' in cmds:
            for connect in all_connections:
                connect.send(str.encode("end.","utf-8"))
                connect.close()
            break
        elif 'help' in cmds:
            print ("The list of available commands:")
            print ("    1) connections\n    2) select\n    3)clear\n    4) exit ")
            print(" Description of <connections> command:\n")
            print(" ------It displays all the connected clients to the server. ------ \n")
            print(" Description of <select> command:\n")
            print(" ------ It allows you to select a partiular client from the list of clients.----\n\t---------FORMAT-----------\n\t select <target>\n")
            print(" Description of <clear> command:\n")
            print(" ------It clears the current screen ------ \n")
            print(" Description of <exit> command:\n")
            print(" ------It exits from the program ------ \n")
        elif cmds == "":
            continue
        elif 'clear' in cmds:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        else:
            print("Invalid Command!!!\nType 'help' to see the list of available commands.")
            continue

def list_connections():
    result = ''
    for i,con in enumerate(all_connections):
        try:
            con.send(str.encode(' '))
            con.recv(10240)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        result+=str(i) + '    ' + str(rno[i]) + '   '+  str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) + '\n'
    print('\tClients\n')
    print(result)

#Selecting Target
def get_target(cmd):
    try:
        target = int(cmd.replace('select ',''))
        print (target)
        conn = all_connections[target]
        print("Now connected to "+str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+'> ',end='')
        return conn
    except:
        print ('Not a valid selection')
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(cmd) > 0:
                conn.send(str.encode(cmd,"utf-8"))
                response = str(conn.recv(10240),"utf-8")
                print(response,end="")
            if cmd == 'quit':
                break
        except:
            print("Connection was lost")
            break

def working():
    for _ in range(NO_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        else:
            prompt()
        queue.task_done()
        break
    exit()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

working()
create_jobs()
