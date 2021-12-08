from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

while 1:
	# Recieve a UDP message
	msg, addr = s.recvfrom(1024)

	# Print the client's MAC Address from the DHCP header
	print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
	for i in range(29, 34):
		print(":" + format(msg[i], 'x'), end = '')
	print()

	#Getting the operation type, which is the first byte of the received message
	opcode = msg[0]

	if(opcode == 0x1):
		print("Handling DHCPDISCOVER (opcode 1): ")
		print("Sending DHCPOFFER...")
		data = get_offer(msg)
		s.sendto(data, DHCP_CLIENT)
	elif(opcode == 0x3):
		print("Handling DHCPREQUEST (opcode 3): ")
		print("Sending DHCPACK...")
		data = get_ack(msg)
		s.sendto(data, DHCP_CLIENT)

# Send a UDP message (Broadcast)
s.sendto('Hello World!', DHCP_CLIENT)

def get_offer(packet):
	OP = bytes([0x02])
	HTYPE = bytes(msg[1])
	HLEN = bytes(msg[2])
	HOPS = bytes(msg[3])
	XID = bytes(msg[4-6])
