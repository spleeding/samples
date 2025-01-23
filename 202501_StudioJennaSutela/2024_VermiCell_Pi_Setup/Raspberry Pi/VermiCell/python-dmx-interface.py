# Studio Jenna Sutela - Vermi Cell 2023-24
# DMX INTERFACE

# This program is called on start up an continously listens for data
# on 127.0.0.1:3010 . The VermiCell PureData  patch  sends information
# about  soundwave amplitudes here.

# It uses Open Light Architecture to send  DMX frames to the strobe.
# It computes a  frame of 512 channels and sends it as an array to
# universe 1.

import socket
import sys
import array
from ola.ClientWrapper import ClientWrapper
from time import sleep

def DmxSent(state):
	wrapper.Stop()


# DMX CONNECTIONS
universe = 1
wrapper = ClientWrapper()
client = wrapper.Client()


# SOCKET NETWORK CONNECTIONS
sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',  3010)
print(f'starting up on {server_address[0]}, port {server_address[1]}') # This just prints a message to terminal.
sock.bind(server_address)
sock.listen(1)


# Core listener loop.
while True:
	print('waiting for connection')
	connection, client_address = sock.accept()
	try:
		while True:
			# Receiving and decoding message, stripping and clearing string before converting to int.				
			data = connection.recv(16)
			data = data.decode("utf-8")
			data = data.replace('\n','').replace('\t','').replace('\r','').replace(';','').replace(' ', '')
			if data:
				data = int(data)
				if 0 <= data < 256:
					frame = array.array('B', [data] * 512)  # Computing array with 512 entries. Int size max 255 because of byte format.
					print(frame[0])
					client.SendDmx(universe, frame, DmxSent)
					wrapper.Run()
					sleep(0.025) # This is set to 40 times per second, which should be correct. I think it is the proper timing for DMX.
				
	# If program is closed on key-board interrupt this is most likely never called.
	# It doesn't really matter because connection is closed automatically after a few  minutes.
	
	finally:
		connection.close() 
