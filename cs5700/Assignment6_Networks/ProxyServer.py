from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Using port 6767
HOST = sys.argv[1]
PORT = 6767
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen()

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print("Message: " + message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print("Filename: " + filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("File To Use: " + filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.read()
        fileExist = "true"
        f.close()
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.sendall(outputdata.encode("utf-8"))
        print('Read from cache')
        # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print("Hostname: " + hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                print("Connected!")
                request = f"GET {filename} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                c.sendall(request.encode())

                buffer = b""
                while True: 
                    data = c.recv(4096)
                    if not data:
                        break
                    buffer += data
                tcpCliSock.sendall(buffer)
                print(buffer)
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                with open("./" + filename, "wb") as tmpFile:
                    tmpFile.write(buffer)
                tmpFile.close()
                c.close()
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send(bytes("HTTP/1.0 404 Not Found\r\n", "utf-8"))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n\r\n", "utf-8"))
            # Close the client and the server sockets
            tcpCliSock.close()
            tcpSerSock.close()