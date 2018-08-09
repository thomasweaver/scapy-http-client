#!/usr/bin/env python

"""
Script to open TCP connection and send 1 HTTP GET request containing
a specific string, and header
Usage:
./http.py <IP_of_target>
There is only one mandatory argument, which is the target IP address.
If other arguments are omitted, will send a preconfigured URL string 
10 times
Optional arguments are : 
./http.py <IP_of_target> |HTTP GET STRING| |Max requests|
e.g.
./http.py 10.10.10.10 'GET / HTTP/1.1\r\n' 100
 """
from scapy.all import *
import random
import sys

dest = sys.argv[1]
try:
    if sys.argv[2]:
        getStr = sys.argv[2]
except :
    getStr = 'GET / HTTP/1.1\r\nHost:' + dest + '\r\nAccept-Encoding: gzip, deflate\r\nX-Test1: lsdhgkhdfgkhdkfgkdgkkdgkhdghdkghkdhf\r\nX-Test2: sglksfglfgljlfgjlkfgfdkgj\r\nX-TEST3: sfksfgsglslgdfgdfgfdgdfgdfg\r\nX-TEST4: fgjkfdkjgdfkgjkdfglkdjflkglks\r\n\r\n'

try:
    if sys.argv[3]:
        max = int(sys.arv[3])

except:
    max = 10

counter = 0
#while counter < max:
#SEND SYN
syn = IP(src="192.168.33.11", dst=dest) / TCP(sport=random.randint(1025,65500), dport=80, flags='S')
#GET SYNACK
syn_ack = sr1(syn)
#Send ACK
out_ack = send(IP(src="192.168.33.11", dst=dest) / TCP(dport=80, sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A'))
#Send the HTTP GET
syn_ack.display()

iterchars = iter(getStr)
ACK=sr1(IP(src="192.168.33.11", dst=dest) / TCP(dport=80, sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr[0])
next(iterchars)

acknum=2
for char in iterchars:
	#ACK.display()
	#print(char)
	send(IP(src="192.168.33.11", dst=dest) / TCP(dport=80, sport=syn_ack[TCP].dport,seq=acknum, ack=acknum + 1, flags='A') / char)
	acknum = acknum +1

