from socket import *
import ssl
import base64
from getpass import getpass

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

username = "OMITTED"
password = "OMITTED"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ('smtp.gmail.com', 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')  
  
# Send HELO command and print server response.
# EHLO needed for TLS
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

starttls_command = 'STARTTLS\r\n'
clientSocket.send(starttls_command.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

# Upgrade to support TLS
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname='smtp.gmail.com')

ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)

# AUTH LOGIN

clientSocket.send(b'AUTH LOGIN\r\n')
recv4 = clientSocket.recv(1024).decode()
print(recv4)

username_encoded = base64.b64encode(username.encode())
clientSocket.send(username_encoded + b'\r\n')
recv5 = clientSocket.recv(1024).decode()
print(recv5)

# Send App Password
password_encoded = base64.b64encode(password.encode())
clientSocket.send(password_encoded + b'\r\n')
recv6 = clientSocket.recv(1024).decode()
print(recv6)

if recv6[:3] == '235':
    print("Authentication successful!")
else:
    print("Authentication failed.")

# Send MAIL FROM command and print server response.
# Fill in start
mailfrom_command = 'MAIL FROM:<OMITTED>\r\n'
clientSocket.send(mailfrom_command.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)

if recv7[:3] != '250':
    print("MAIL FROM FAILED")

# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
rcpt_command = 'RCPT TO:<OMITTED>\r\n'
clientSocket.send(rcpt_command.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)

if recv8[:3] != '250':
    print("RCPT TO FAILED")
# Fill in end

# Send DATA command and print server response.
# Fill in start
data_command = 'DATA\r\n'
clientSocket.send(data_command.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '354':
    print("DATA command failed")
# Fill in end

# Send message data.
# Fill in start
msg = (
    "From: " + username + "\r\n"
    "To: " + username + "\r\n"
    "Subject: assignment 5\r\n"
    "\r\n"
    "I love computer networks!\r\n"
)
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)

if recv10[:3] != '250':
    print("Email couldn't send")
# Fill in end

# Message ends with a single period.
# Fill in start

# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send(b'QUIT\r\n')
recv11 = clientSocket.recv(1024).decode()
print(recv11)
clientSocket.close()
