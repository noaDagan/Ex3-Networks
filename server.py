#Noa Dagan 311302137
#Nofar Bar-zakai 205643638
import socket, threading
import sys
import os

# open socket to connect with the clients with port from the usr
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip ='0.0.0.0'
dest_port = int(sys.argv[1])
server.bind((server_ip, dest_port))
server.listen(5)

# wait for client to connect
while True:
	connection = True
	client_socket, client_address = server.accept()
	#While The client is connected
	while connection:
		#Set timeout 1 second to recive the data
		client_socket.settimeout(1)
		try:
			data = client_socket.recv(1024)
		except socket.timeout:
			print "Time Out"
			client_socket.close()
			break
		#Print all the message
		print data
		#Split the lines 
		lines = data.split("\r\n")
		connect_param = ""
		is_redirect = False
		to_bit = False
		file_name = ""
		path = ""
		#Go over all the lines from the data
		for line in lines:
			line = line.split(' ')
			#If the line is Get request
			if line[0] == "GET":
				if line[2] != "HTTP/1.1":
					print "ERROR"
				file_name = line[1]
				if file_name == "/redirect":
					is_redirect = True
					break
				if file_name == '/':
					file_name = "./files/index.html"
					path = file_name
					break
				else: 
					file_name = "./files" + line[1]
				path_file = "./files"
				#Go over all the files in the files directory and search for the file name recived
				for root,dirs,files in os.walk(path_file):
					for file in files:
						new_path = root + '/' + str(file)
						if file_name == new_path:
							if file.endswith('.jpg') or file.endswith('.ico'):
								to_bit = True
							path = root + '/' + str(file)
							break
			#Check the coonection -close or keep alive
			elif line[0] == "Connection:":
				connect_param = line[1]
				if connect_param == "close":
					connection = False
		#If the file is redirect return the file result.hrml
		if is_redirect:
			connection = False
			str_send = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n"
			client_socket.send(str_send)
		# file not exit
		elif path == "":
			connection = False
			str_send = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n"
			client_socket.send(str_send)
		else:
			#Return the file to the client
			length_file = os.path.getsize(path)
			str_send = "HTTP/1.1 200 OK\r\nConnection: "+ str(connect_param) +"\r\n"+ "Content-Length: " + str(length_file) + "\r\n\r\n"
			#Check if the file is jpg or ico
			if to_bit == True:
				file_to_read = open(path,'rb')  
			else:
				file_to_read = open(path,'r')  
			line = file_to_read.read(1024)
			# read the file and send
			while line:
				str_send = str_send + line
				line = file_to_read.read(1024)
			client_socket.send(str_send)
	# close the socket
	client_socket.close()
