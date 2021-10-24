import socket
import threading


nickname = input('choose a nickname:')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'please enter your nickname:':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('an error occurred!')
            client.close()


def write():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()





