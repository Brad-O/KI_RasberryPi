#!/usr/bin/python
import socket
import struct
import math
import time

echoCmd = 1

def instrConnect(mySocket, myAddress, myPort, timeOut, doReset, doIdQuery):
    mySocket.connect((ipAddress, port)) # input to connect must be a tuple
    mySocket.settimeout(timeOut)
    if doReset == 1:
        #mySocket.send("*RST\n".encode())
        instrSend(mySocket, "*RST")
    if doIdQuery == 1:
        print(instrQuery(mySocket, "*IDN?", 100))
        #mySocket.send("*IDN?\n".encode())
        #print(mySocket.recv(100).decode())
    return mySocket

def instrDisconnect(mySocket):
    mySocket.close()
    return

def instrSend(mySocket, cmd):
    if echoCmd == 1:
        print(cmd)
    cmd = "{0}\n".format(cmd)
    mySocket.send(cmd.encode())
    return

def instrQuery(mySocket, cmd, rcvSize):
    instrSend(mySocket, cmd)
    return mySocket.recv(rcvSize).decode()
    
#===== MAIN PROGRAM STARTS HERE =====
ipAddress = "169.254.62.134"
port = 5025
timeout = 20.0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = instrConnect(s, ipAddress, port, timeout, 1, 1)

t1 = time.time()

for j in range(1, 28800):
    t3 = time.time()
    time.sleep(9.25)
    instrSend(s, "ROUTE:OPEN:ALL")
    instrSend(s, "TRAC:CLE")
    instrSend(s, "FORM:DATA ASCII")
    instrSend(s, "FUNC 'TEMP', (@101:110)")
    instrSend(s, "TEMP:TRAN TC, (@101:110)")
    instrSend(s, "TEMP:TC:TYPE J, (@101:110)")
    instrSend(s, "TEMP:TC:RJUN:RSEL INT, (@101:110)")
    instrSend(s, "ROUT:SCAN:COUN:SCAN 1")
    instrSend(s, "ROUT:SCAN:INT 0")
    instrSend(s, "ROUT:SCAN:CRE (@101:110)")
    instrSend(s, "DISP:WATC:CHAN \"101:110\"")
    instrSend(s, "INIT")
    print(instrQuery(s, "*OPC?", 8))
    rcvBuffer = instrQuery(s, "TRAC:DATA? 1, 10, \"defbuffer1\", READ, REL, CHAN", 1024)
    rcvBuffer2 = rcvBuffer.split(',')
    #print(len(rcvBuffer2))
    #print(rcvBuffer)
    #print(rcvBuffer2)
    i = 0
    while i < len(rcvBuffer2):
        infoData = "{0}, {1}, {2}".format(rcvBuffer2[i], rcvBuffer2[i+1], rcvBuffer2[i+2])
        print(infoData)
        i += 3
    t4 = time.time()
    print("{0:.6f} s".format(t4-t3))
    t5 = time.time()
    print("Total Time {0:.6f} s".format(t5-t1))
    
instrDisconnect(s)

t2 = time.time()

# Notify the user of completion and the test time achieved. 
print("done")
print("{0:.6f} s".format(t2-t1))
input("Press Enter to continue...")
exit()



