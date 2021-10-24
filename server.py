import threading
import socket

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcasting_for_group_chat(message):
    for client in clients:
        client.send(message.encode('utf-8'))


def handle_for_group_chat(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == f'{nickname}: CHANGE ROOM':
                message = ask_with_whom_you_wanna_connect(client)

                connect_to_group_or_private_chat(client, nickname, message)
            else:
                broadcasting_for_group_chat(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcasting_for_group_chat(f"{nickname} left the chat")
            nicknames.remove(nickname)
            break


def sender_for_two_clients(client, message):
        try:
            client.send(message.encode('utf-8'))
        except:
            client.close()


def ask_with_whom_you_wanna_connect(client):
    client.send('Here are nicknames of connected users,'
                ' please select with whom you want to send message\n'.encode('utf-8'))
    for nick in nicknames:
        client.send((f"{nicknames.index(nick)} {nick}\n".encode('utf-8')))
    client.send('or enter group chat, typing \'GROUP\''.encode('utf-8'))
    message = client.recv(1024).decode('utf-8')
    return message


def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send("please enter your nickname:".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        message = ask_with_whom_you_wanna_connect(client)

        connect_to_group_or_private_chat(client, nickname, message)


def connect_to_group_or_private_chat(client, nickname, message):

    if message == f'{nickname}: GROUP':
        broadcasting_for_group_chat(f'{nickname} joined the chat!')
        client.send('You are connected to group chat feel free to chat!'.encode('utf-8'))
        thread = threading.Thread(target=handle_for_group_chat, args=(client, nickname))
        thread.start()

    else:
        client2 = clients[int(message[-1])]
        client.send(
            f'You are connected to {nicknames[int(message[-1])]}, write your message to him/her'.encode('utf-8'))
        while True:
            message = client.recv(1024).decode('utf-8')
            if message == f'{nickname}: CHANGE ROOM':
                message = ask_with_whom_you_wanna_connect(client)
                connect_to_group_or_private_chat(client, nickname, message)
            else:
                thread = threading.Thread(target=sender_for_two_clients, args=(client2, message))
                thread.start()


receive()
