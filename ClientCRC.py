import socket
import os
import sys
import binascii

crc_gen = b'11000000000000101' # Define CRC polynomial as binary



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


    while True:
	data = raw_input("Enter data you want to send: ") # Capture data

	data_word = (''.join(format(ord(x), 'b') for x in data)) # Convert data to binary 
	print ("Data word in binary: " + data_word)


	n = len(str(crc_gen)) # Length of CRC generator polynomial


	data_bin = list(data_word) # Convert data to list,
	crc = list(crc_gen) 	   # So we can reach any bit easily
	

	for i in range(0,n-1): # Append n-1 bits to binary data
		data_bin.append('0')


	print("Data for XOR: ",data_bin) # Print data before division
	print("\n")
		
	m = len(data_bin) # 'm' is length of dividend data
	temp = list()
	end_result = list()

	print("m: ", m, " n: ",n) # 'm' is length of data, 'n' is length of CRC 


	offset = n # 'offset' determines how many bits of data calculated for division at a time

	for i in range(0,n): # Fetch bits to 'temp' for operation, 'temp' is dummy for division operation
		temp.append(data_bin[i])

	
	
	while(offset<len(data_bin)): # Execute until completion of all data		
		print("Temp: ", temp)
		print("\n")
		

		print("CRC: ", crc)
		print("\n")

		for i in range(0, n):
			temp[i] = xor(temp[i], crc[i]) # Execute XOR

	
		print("Result of iteration: ",temp) # Intermediate result

	
		while(temp[0] == '0'): # If prefix of temp is zero, discard them and get some bits from data
			if(offset == m):
				break
			print(offset)
			print(temp)
			for i in range(0, n-1):
				temp[i] = temp[i+1]
			temp[n-1] = data_bin[offset]
			offset = offset + 1
			if(offset == m):
				break

		if(offset >= len(data_bin)): 
			
			for i in range(1,n):
				end_result.append(temp[i])	# Find CRC value, now division has completed.
								# No need to variable 'temp' anymore
			
			
	

		print("New temp:", temp)
		print("\n \n")
		
	for i in range(0,len(end_result)):
		data_bin[m-i-1] = end_result[len(end_result) - i -1]	# Append CRC to data  
		

	print("CRC Found: ", end_result)
	print("Sending data: ", data_bin)
	send_data = ''.join(data_bin) 	# Convert result to string 
	s.sendto(send_data,(host,port)) # Send resulted data to server
	
	
	data, addr = s.recvfrom(2048)
	print("Received Data: ", data)

	check = data_word # It is checking parameter 

	for i in range(0,n-1):	# Append zeros to check
    		check+=str("0")	# If received data is correct, CRC field should be zero
	
	if(data == check):	# Check if received data is correct
		print("DONE ,NO ERROR")
	else:
		print("ERROR")

    	s.close()
	break



if __name__ == '__main__':
    Main()
