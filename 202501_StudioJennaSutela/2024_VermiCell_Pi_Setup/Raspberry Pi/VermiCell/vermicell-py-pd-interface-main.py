# Studio Jenna Sutel - Vermi Cell 2023-24
# Python-Pure-Data Interface 

# This script reads electrical current sent from a battery
# the voltage is mapped to a value between 0 and 1023 based
# on a reference voltage of 3v3.

# Example  input: 1.4v maps to around 431 (one AAA batterxy).
# There willbe  some disturbances from the currents passing through
# the  circuit, but not enough that it will  have a  noticable impact
# on the readings.   

# The only actual library needed is spidev. Updates a  few  times  a year.
import sys
from time import sleep
import spidev # type: ignore - and remember to install this in the correct venv on the PI
import socket

# Network (localhost) vaiables: for communicating with PureData
UDP_IP = "127.0.0.1"
UDP_PORT = 3000

# Variables: Data to send and delay.
data  = 0
dly = 1

# SPI interface set up:
spi = spidev.SpiDev() #Create a SpiDev object
spi.open(0, 0) # Opening SPI device  on /dev/spidev0.0 which is also chip select 0.
spi.max_speed_hz = 500000 # I read multiple places this should be  kept high for the chip to function properly. Some say even 1350000.
spi.mode = 0


# Define a function  to read data from the MCP3008 device. ADC means Analog to Digital Converter.
def read_adc(mcp_channel):
	# Send three bytes: a start bit for MCP3008, a second byte specifying its a single ended mode and channel num, a third byte is just trailing zeroes.
	msg = [0b01, (0b1000 + mcp_channel) << 4, 0b00]
	response = spi.xfer2(msg) # xfer2 is a write/read function that sends a message and reads a  response. Both msg and response  are arrays.
	
	adc_value = ((response[1] & 0b11) << 8) + response[2] # Combining  the second  and last entry in the  response. Using binary  logic, similar to the operations in the patch.
	return adc_value


# Instantiate socket network operations.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
		
		# Read the value  from the  MCP3008 on the pin we specified in analogPort to data var.
		data = read_adc(0) # Reading channel 0 on MCP3008
		
		sock.sendto(data.to_bytes(2,byteorder='big'), (UDP_IP,UDP_PORT)) # Send data over udp, localhost.
		
		print(data)
		print(data.to_bytes(2, byteorder='big'))
		
		
		sleep(dly) # To add an ms between each iteration.
		
except KeyboardInterrupt:
	sys.exit()
		
