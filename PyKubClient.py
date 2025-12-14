import socket

# Source - https://stackoverflow.com/a/3462840
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
# Retrieved 2025-12-11, License - CC BY-SA 4.0

host = ''
port = ''
sock = socket.socket()
sock.settimeout(5)
while(True):
    while(True):
        host = input('Enter host IP: ')
        if(validate_ip(host)):
            break
        print('Invalid format. ', end = '')
    while(True):
        port = input('Enter port: ')
        if(port.isdigit()):
            port = int(port)
            break
        print('Invalid, must be positive integer. ', end = '')
    print('Attempting to establish connection to (\'', host, '\', ', port, ')', sep = '')
    try:
        sock.connect((host, port))
        print('Successfully connect to ', sock.getpeername(), sep = '')
        break
    except TimeoutError:
        print('Timeout.')
sock.settimeout(None)
while(True):
    data = sock.recv(1024)
    if(not data):
        break
    text = data.decode()
    print(text, end = '')
    if(text[-1] == '\u0005'):
        text = input().lower()
        sock.sendall(text.encode())
sock.close()