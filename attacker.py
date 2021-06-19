# Import socket module
import socket

# Import pickle module
import pickle

# Import randint function from random module
from random import randint

# Import generateHammingCode function from HammingCode module
from HammingCode import generateHammindCode

# import datetime function from datetime module
from datetime import datetime


HEADER_SIZE = 10


# function that convert a string to binary and return as a list
def strToBinary(s):
    bin_conv = []
    for c in s:
        # convert each char to ASCII value
        ascii_val = ord(c)
        # Convert ASCII value to binary
        binary_val = bin(ascii_val)
        # add binary_val to a bin_cov list
        bin_conv.append(binary_val[2:])
    return bin_conv


# send an encoded message to defender
def sendMessageEncoded(client_Socket, message,timestamp):
    scrambled = []
    scrambled_msg = []
    # using the generateHammingCode to encode every character to a hamming code.
    for d in strToBinary(message):
        data = str(generateHammindCode(d))
        scrambled.append(data)

    # generate a random number between 0 and 8 using the randint function
    rand = randint(0, 8)
    rand1 = randint(0, 8)
    # Using the rand number to flip bits in the hamming code of every
    # character which will be the index of a bit in a sequence
    for data in scrambled:
        scramble = []
        for i in data:
            scramble.append(i)

        if scramble[len(scramble) - 1 - rand] == '0':
            scramble[len(scramble) - 1 - rand] = '1'
        else:
            scramble[len(scramble) - 1 - rand] = '0'

        if scramble[rand1] == '0':
            scramble[rand1] = '1'
        else:
            scramble[rand1] = '0'

        scrambled_msg.append(''.join(scramble))

    # put scrambled message and the timestamp in a dictionary d
    d = {'scrambled_msg': scrambled_msg,
         'rtt': timestamp}

    msg = pickle.dumps(d)

    # msg is now the message itself in addition to the header
    msg = bytes(f'{len(msg):<{HEADER_SIZE}}', "utf-8") + msg

    # show sent messages
    print("original message: ", strToBinary(message))
    print("scrambled message: ", d['scrambled_msg'])

    # send the message to the client.
    client_Socket.send(msg)


MESSAGE = "ATTACK"

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to the port
s.bind((socket.gethostname(), 1500))

# Now wait for client connection.
s.listen(5)

# an infinite loop until we interrupt it or an error occurs
while True:
    now = datetime.now()
    # Establish connection with client.
    clientSocket, address = s.accept()
    print(f"Connection to {address} established")
    sendMessageEncoded(clientSocket, MESSAGE,datetime.timestamp(now))
    while True:
        now = datetime.now()
        from_client = clientSocket.recv(1024).decode()
        print("=============================================")
        print("=============================================")
        print()
        # if the attacker receive a 'again' send an attack message again
        if from_client == 'again':
            print('Let us play again.')
            sendMessageEncoded(clientSocket, MESSAGE,datetime.timestamp(now))
        # otherwise close the socket
        else:
            break

    clientSocket.close()
    break
