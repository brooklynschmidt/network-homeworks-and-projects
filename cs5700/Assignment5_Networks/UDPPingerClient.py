from socket import *
from datetime import datetime

clientSocket = socket(AF_INET, SOCK_DGRAM)

# 1 second timeout
clientSocket.settimeout(1.0)

# Server address
serverAddress = ('127.0.0.1', 12000)

rtt_list = []
packets_lost = 0

for i in range(1, 11):
    try:
        start_time = datetime.now()
        # Client msg is Ping sequence_number time
        msg = "Ping " + str(i) + " " + str(start_time)
        msg_bytes = msg.encode()
        # Send ping message using UDP
        clientSocket.sendto(msg_bytes, serverAddress)

        message, address = clientSocket.recvfrom(1024)
        end_time = datetime.now()

        rtt = end_time - start_time
        str_message = message.decode()

        # Print server response if there is one
        # Calculate and print RTT
        print(str_message + " | RTT: " + str(rtt) + " or " + "0." + str(rtt.microseconds) + "ms")
        rtt_list.append(rtt.microseconds)

    except TimeoutError:
        # otherwise, print "request timed out"
        print("Request timed out")
        packets_lost += 1

print("---------------")
print("Ping Statistics")
print("---------------")
min_rtt = min(rtt_list)
max_rtt = max(rtt_list)
avg_rtt = sum(rtt_list) / len(rtt_list)
packet_loss = (packets_lost / 10) * 100

print("Minimum RTT: " + "0." + str(min_rtt) + "ms")
print("Maximum RTT: " + "0." + str(max_rtt) + "ms")
print("Average RTT: " + "0." + str(avg_rtt) + "ms")
print("Packet Loss (%): " + str(packet_loss) + "%")
clientSocket.close()


