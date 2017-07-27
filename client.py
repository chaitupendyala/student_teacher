import os
import socket
import subprocess

s = socket.socket()
host = '127.0.0.1'
port = 9999 # port tells us what data is actually coming in
roll_no=input("Enter you roll number: ")
s.connect((host,port))
#roll_data = str(roll_no,"utf-8")
s.send(str.encode(roll_no,"utf-8"))
log = open("logfile.txt","w")
mess = s.recv(1024)
mess = str(mess,"utf-8")
print (mess)
if mess == "Already connected to the server\nPlease wait for your turn.":
    s.close()
    exit()
while True:

    data = s.recv(1024)
    print("Server is typing...")
    commands=data.decode("utf-8")
    log.write(commands + '\n')
    print(commands +'\n')
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if data[:4].decode("utf-8") == 'quit':
       print ("Server is now attending another client.\nPlease wait :)")
    if commands == "end.":
        break
    elif len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read() # this is the byte version of the output and this is sent to the server
        output_str = str(output_byte,"utf-8")   # this is the client version and is used to print it here
        s.send(str.encode(output_str+ str(os.getcwd()) + ': ',"utf-8"))

log.close()
#close connection
s.close()
