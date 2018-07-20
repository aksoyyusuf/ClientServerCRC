import socket
import os
import sys
import binascii

crc_gen = b'11000000000000101' # Define CRC polynomial
#crc_gen = b'1101'


def xor(a,b): # XOR operation for 1-bit
    result = []
    if a != b:
        result = '1'
    else:
        result = '0'
    return result

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = "127.0.0.1"
    port = 10000
    s.bind((host,port))


    print("Server Started")

    while True:
	data, addr = s.recvfrom(1024)
	print("Client connected  ip:<" + str(addr) + ">")
	print("Received data: ", data)

	data_word = bin(int(data,2))[2:] # Convert data to binary 

	print("Data word", data_word)

	n = len(str(crc_gen)) # Length of crc generator polynomial


	data_bin = list(data_word) # Convert data to list,
	crc = list(crc_gen) 	   # So we can reach any bit easily
	
	


	print("Data for XOR: ",data_bin)
	print("\n")
		
	m = len(data_bin) # 'm' is length of dividend data
	temp = list()
	end_result = list()

	print("m: ", m, " n: ",n)


	offset = n
	for i in range(0,n): # Fetch bits to temp for operation
		temp.append(data_bin[i])


	while(offset<len(data_bin)):	# Execute until completion of all data	
		print("Temp: ", temp)
		print("\n")
		

		print("CRC: ", crc)
		print("\n")

		for i in range(0, n):
			temp[i] = xor(temp[i], crc[i])	# Execute XOR

	
		print("Result of iteration: ",temp)


	
		while(temp[0] == '0'):		# If prefix of temp is zero, discard them and get some bits from data
			if(temp[0] == '0'):
				print(offset)
				print(temp)
				for i in range(0, n-1):
					temp[i] = temp[i+1]
				temp[n-1] = data_bin[offset]
				offset = offset + 1
				if(offset == len(data_bin)):
					break


		if(offset >= len(data_bin)):
			for i in range(1,n):
				end_result.append(temp[i])	
			
	

		print("New temp:", temp)
		print("\n \n")
		
	for i in range(0,len(end_result)):
		data_bin[m-i-1] = end_result[len(end_result) - i -1]

	print("CRC Found: ", end_result)
	print("Sending data: ", data_bin)
	


	check = list()
	for i in range(0, n-1):		# Append zeros to check
		check.append('0')	# If received data is correct, CRC field should be zero
	print("Check: ", check)

	end = ''.join(end_result) # Convert result to string 
	send_data = ''.join(data_bin)	# Send resulted data to server
	

	if(end_result == check):	# Check if received data is correct
		print("DONE, NO ERROR")
		print("CRC: ", end)
	else:
		print("DATA CORRUPTED, ERROR")
	
	s.sendto(send_data, addr) # Send data to client
	print("DATA SENT")

    	s.close()
	break

if __name__ == '__main__':
    Main()
