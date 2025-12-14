from random import randint
from sys import exit
import socket

def id_to_kub(id):
    if id == 0:
        return('F00')
    if   (id - 1) // 13 == 0:
        kubType='A'
    elif (id - 1) // 13 == 1:
        kubType='B'
    elif (id - 1) // 13 == 2:
        kubType='C'
    else:
        kubType='D'
    return(kubType + str((id - 1) % 13 + 1).rjust(2, '0'))

def kub_to_id(kub):
    kub = kub.upper()
    if kub == 'F00' or kub == 'F':
        return(0)
    if len(kub) < 2 or len(kub) > 3:
        return(-1)
    if len(kub) == 2:
        kub = list(kub)
        kub.insert(1, '0')
        kub = ''.join(kub)
    if ord(kub[0]) < 65 or ord(kub[0]) > 68 or (ord(kub[1]) - 48) * 10 + ord(kub[2]) - 48 < 1 or (ord(kub[1]) - 48) * 10 + ord(kub[2]) - 48 > 13:
        return(-1)
    return((ord(kub[0]) - 65) * 13 + int(kub[1]) * 10 + int(kub[2]))

def has_repeat_item(inputList, exception = None):
    temporarySet = set()
    for i in inputList:
        if i != exception:
            temporarySet.add(i)
    return len(inputList) - inputList.count(exception) != len(temporarySet)

def print_stack_info():
    broadcast('Table:\n')
    if len(table) == 0:
        broadcast('None\n')
    else:
        for i in range(len(table)):
            broadcast(str(i + 1) + ': ')
            for j in table[i]:
                broadcast(id_to_kub(j) + ' ')
            broadcast('\n')
    player_print('Your stack:\n')
    for i in range(len(playerStack[playerId])):
        player_print(id_to_kub(playerStack[playerId][i]) + ' ')
    player_print('\nBroke ice: ' + str(playerBreakIce[playerId]) + '\n')
    broadcast('\n')

def play_kubset():
    for i in command:
        try:
            playerStack[playerId].remove(i)
            kubSetCheck.append(i)
        except:
            print('Invalid: Your stack doesn\'t have enough Kubs to form the Kubset')
            playerStack[playerId].extend(kubSetCheck)
            playerStack[playerId].sort()
            break
    else:
        playerBreakIce[playerId] = True
        table.append([])
        for i in command:
            table[-1].append(i)
        print_stack_info()
    kubSetCheck.clear()

def broadcast(text):
    print(text, end = '')
    connection.sendall(text.encode())

def player_print(text):
    if(playerId == 0):
        print(text, end = '')
    else:
        connection.sendall(text.encode())

def get_player_name():
    if(playerId == 0):
        return('Host')
    else:
        return('Client')

#initialize
table = []
stack = []
playerStack = []
playerBreakIce = []
playerAmount = 2 #fixed for this version
playerId = 0
shouldDraw = True
command = []
kubSetCheck = []
sock = socket.socket()
sock.bind(('', 0))
print('Waiting connection to this device: (\'', socket.gethostbyname(socket.gethostname()), '\', ', sock.getsockname()[1], ')', sep = '')
sock.listen(1)
connection, addr_info = sock.accept()
print('Successfully connected by', addr_info)
LINE = '-------------------------\n'
for i in range(53):
    stack.append(i)
    stack.append(i)
for i in range(playerAmount):
    playerStack.append([])
    for j in range(14):
        playerStack[i].append(stack.pop(randint(0, len(stack) - 1)))
    playerStack[i].sort()
    playerBreakIce.append(False)
broadcast('<GAMESTART>\n')

#main
while(stack != [] and ([] not in playerStack)):
    if playerId >= playerAmount:
        playerId = 0
    broadcast(get_player_name() + '\'s turn begins.\n')
    print_stack_info()
    while True:
        player_print(LINE + 'Please enter command:\n')
        if(playerId == 0):
            command = input().lower().split()
        else:
            connection.sendall('\u0005'.encode())
            data = connection.recv(1024)
            command = data.decode().split()
        player_print(LINE)
        if   command[0] == 'exit':
            broadcast(get_player_name() + ' has exited the game.\n')
            connection.close()
            sock.close()
            exit()
        elif command[0] == 'end':
            if shouldDraw == True:
                playerStack[playerId].append(stack.pop(randint(0,len(stack)-1)))
                playerStack[playerId].sort()
            break
        elif command[0] == 'info':
            print_stack_info()
        elif command[0] == 'take':
            if playerBreakIce[playerId] == False:
                player_print('Invalid: Havn\'t break ice yet\n')
            elif len(command) == 1:
                player_print('Invalid: No argument found after \"take\"\n')
            else:
                try:
                    for i in table.pop(int(command[1]) - 1):
                        playerStack[playerId].append(i)
                    playerStack[playerId].sort()
                    shouldDraw = False
                    print_stack_info()
                except:
                    player_print('Invalid: Only accepts integer in range(table length) as index\n')
        elif command[0] == 'play':
            if len(command) == 1:
                player_print('Invalid: No argument found after \"play\"\n')
            else:
                command = list(map(kub_to_id, command))
                command.sort()
                while -1 in command:
                    command.remove(-1)
                if len(command) < 3:
                    player_print('Invalid: Not enough valid Kubs are found\n')
                elif has_repeat_item(command, 0):
                    player_print('Invalid: Any Kubset can\'t contains two same Kubs except Freekubs\n')
                else:
                    for i in command:
                        if i != 0:
                            kubSetCheck.append(id_to_kub(i)[0])
                    if not has_repeat_item(kubSetCheck):
                        kubSetCheck.clear()
                        for i in command:
                            if i != 0:
                                kubSetCheck.append((i - 1) % 13 + 1)
                        if len(set(kubSetCheck)) == 1:
                            if kubSetCheck[0] * len(command) >= 30 or (len(kubSetCheck) == 1 and kubSetCheck[0] == 9) or playerStack[playerId][0] == True:
                                kubSetCheck.clear()
                                play_kubset()
                                shouldDraw = False
                            else:
                                player_print('Invalid: Can\'t break ice with this Kubset (Sum<30)\n')
                        else:
                            player_print('Invalid: This N-type Kubset contains different numbers\n')
                            kubSetCheck.clear()
                    elif len(set(kubSetCheck)) == 1:
                        kubSetCheck.clear()
                        for i in range(len(command) - 1):
                            if command[i] == 0:
                                continue
                            if command[i] + 1 != command[i + 1]:
                                if 0 in command:
                                    command[0] = None
                                    kubSetCheck.append(0)
                                else:
                                    player_print('Invalid: This G-type Kubset isn\'t continuous\n')
                                    break
                        else:
                            while None in command:
                                command.remove(None)
                            if 0 in kubSetCheck:
                                for i in range(len(command) - 1):
                                    if command[i] + 1 != command[i + 1]:
                                        command.insert(i, kubSetCheck.pop())
                                if kubSetCheck != []:
                                    while 0 in kubSetCheck:
                                        command.insert(0, kubSetCheck.pop())
                            kubSetCheck = [13, 0]
                            for i in command:
                                if i != 0 and (i - 1) % 13 + 1 < kubSetCheck[0]:
                                    kubSetCheck[0] = (i - 1) % 13 + 1
                            for i in command:
                                if i != 0 and (i - 1) % 13 + 1 > kubSetCheck[1]:
                                    kubSetCheck[1] = (i - 1) % 13 + 1
                            if sum(range(kubSetCheck[0], kubSetCheck[1] + command.count(0) + 1)) >= 30 or playerBreakIce[playerId]:
                                kubSetCheck.clear()
                                play_kubset()
                                shouldDraw = False
                            else:
                                player_print('Invalid: Can\'t break ice with this Kubset (Sum<30)\n')
                    else:
                        player_print('Invalid: This Kubset is neither N-type nor G-type\n')
        else:
            player_print('Unknown command. Please retry with \"play\" or \"take\".\n')
    broadcast(get_player_name() + '\'s turn ends.\n\n')
    shouldDraw = True
    kubSetCheck.clear()
    playerId += 1
broadcast('<GAMEOVER>\nWinner:')
if stack == []:
    broadcast('Stack\n')
else:
    for i in playerStack:
        if i == []:
            playerId = i
            break
    broadcast(get_player_name() + '\n')
connection.close()
sock.close()