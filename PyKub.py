#Functions
from random import randint
from time import sleep
def idToKub(id):
    if id==0:
        return('F00')
    if (id-1)//13==0:
        kubType='A'
    elif (id-1)//13==1:
        kubType='B'
    elif (id-1)//13==2:
        kubType='C'
    else:
        kubType='D'
    return(kubType+str((id-1)%13+1).rjust(2,'0'))
def kubToId(kub):
    kub=kub.upper()
    if kub=='F00' or kub=='F':
        return(0)
    if len(kub)<2 or len(kub)>3:
        return(-1)
    if len(kub)==2:
        kub=list(kub)
        kub.insert(1,'0')
        kub=''.join(kub)
    if ord(kub[0])<65 or ord(kub[0])>68 or (ord(kub[1])-48)*10+ord(kub[2])-48<1 or (ord(kub[1])-48)*10+ord(kub[2])-48>13:
        return(-1)
    return((ord(kub[0])-65)*13+int(kub[1])*10+int(kub[2]))
def listHasRepeatItem(inputList,exception=None):
    temporarySet=set()
    for i in inputList:
        if i!=exception:
            temporarySet.add(i)
    return len(inputList)-inputList.count(exception)!=len(temporarySet)
def printStackInfo():
    print('Table:')
    if len(table)==0:
        print('None')
    else:
        for i in range(len(table)):
            print(i+1,": ",end='')
            for j in table[i]:
                print(idToKub(j),end=' ')
            print()
    print('Your stack:')
    for i in range(1,len(playerStack[playerId])):
        print(idToKub(playerStack[playerId][i]),end=' ')
    print('\nBreak ice :',playerBreakIce[playerId])
def playKubset():
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
        playerBreakIce[playerId]=True
        table.append([])
        for i in command:
            table[-1].append(i)
        printStackInfo()
    kubSetCheck.clear()
#Initialize
table=[]
stack=[]
playerStack=[]
playerBreakIce=[]
playerAmount=input('Please enter player amount:\n')
playerId=0
shouldDraw=True
command=[]
kubSetCheck=[]
while True:
    try:
        playerAmount=int(playerAmount)
        if playerAmount>=2 and playerAmount<=4:
            break
        else:
            playerAmount=input('Invalid: Must between 2 and 4; Please retry:\n')
    except:
        playerAmount=input('Invalid: Must be integer\nPlease retry:\n')
for i in range(53):
    stack.append(i)
    stack.append(i)
for i in range(playerAmount):
    playerStack.append([])
    for j in range(14):
        playerStack[i].append(stack.pop(randint(0,len(stack)-1)))
        playerStack[i].sort()
    playerBreakIce.append(False)
print('<GAMESTART>')
#Main loop
while(stack!=[] and ([] not in playerStack)):
    if playerId>=playerAmount:
        playerId=0
    print('Player#',playerId+1,'\'s turn begins.',sep='')
    printStackInfo()
    while True:
        command=input('-------------------------\nPlease enter command:\n').lower().split()
        print('-------------------------')
        if command[0]=='end':
            if shouldDraw==True:
                playerStack[playerId].append(stack.pop(randint(0,len(stack)-1)))
                playerStack[playerId].sort()
            break
        elif command[0]=='info':
            printStackInfo()
        elif command[0]=='take':
            if playerBreakIce[playerId]==False:
                print('Invalid: Havn\'t break ice yet')
            elif len(command)==1:
                print('Invalid: No argument found after \"take\"')
            else:
                try:
                    for i in table.pop(int(command[1])-1):
                        playerStack[playerId].append(i)
                    playerStack[playerId].sort()
                    shouldDraw=False
                    printStackInfo()
                except:
                    print('Invalid: Only accepts integer in range(table length) as index')
        elif command[0]=='play':
            if len(command)==1:
                print('Invalid: No argument found after \"play\"')
            else:
                command=list(map(kubToId,command))
                command.sort()
                while -1 in command:
                    command.remove(-1)
                if len(command)<3:
                    print('Invalid: Not enough valid Kubs are found')
                elif listHasRepeatItem(command,0):
                    print('Invalid: Any Kubset can\'t contains two same Kubs except Freekubs')
                else:
                    for i in command:
                        if i!=0:
                            kubSetCheck.append(idToKub(i)[0])
                    if not listHasRepeatItem(kubSetCheck):
                        kubSetCheck.clear()
                        for i in command:
                            if i!=0:
                                kubSetCheck.append((i-1)%13+1)
                        if len(set(kubSetCheck))==1:
                            if kubSetCheck[0]*len(command)>=30 or (len(kubSetCheck)==1 and kubSetCheck[0]==9) or playerStack[playerId][0]==True:
                                kubSetCheck.clear()
                                playKubset()
                                shouldDraw=False
                            else:
                                print('Invalid: Can\'t break ice with this Kubset (Sum<30)')
                        else:
                            print('Invalid: This N-type Kubset contains different numbers')
                            kubSetCheck.clear()
                    elif len(set(kubSetCheck))==1:
                        kubSetCheck.clear()
                        for i in range(len(command)-1):
                            if command[i]==0:
                                continue
                            if command[i]+1!=command[i+1]:
                                if 0 in command:
                                    command[0]=None
                                    kubSetCheck.append(0)
                                else:
                                    print('Invalid: This G-type Kubset isn\'t continuous')
                                    break
                        else:
                            while None in command:
                                command.remove(None)
                            if 0 in kubSetCheck:
                                for i in range(len(command)-1):
                                    if command[i]+1!=command[i+1]:
                                        command.insert(i,kubSetCheck.pop())
                                if kubSetCheck!=[]:
                                    while 0 in kubSetCheck:
                                        command.insert(0,kubSetCheck.pop())
                            kubSetCheck=[13,0]
                            for i in command:
                                if i!=0 and (i-1)%13+1<kubSetCheck[0]:
                                    kubSetCheck[0]=(i-1)%13+1
                            for i in command:
                                if i!=0 and (i-1)%13+1>kubSetCheck[1]:
                                    kubSetCheck[1]=(i-1)%13+1
                            if sum(range(kubSetCheck[0],kubSetCheck[1]+command.count(0)+1))>=30 or playerBreakIce[playerId]:
                                kubSetCheck.clear()
                                playKubset()
                                shouldDraw=False
                            else:
                                print('Invalid: Can\'t break ice with this Kubset (Sum<30)')
                    else:
                        print('Invalid: This Kubset is neither N-type nor G-type')
        else:
            print('Unknown command. Please retry with \"play\" or \"take\".')
    for i in range(50):#Sensor previous player's information
        print()
    print('Player#',playerId+1,'\'s turn Ends.\nChanging player after 5 seconds...',sep='')
    for i in range(5):#Delay before next player's turn
        print(5-i,'...',sep='',end='')
        sleep(1)
    print()
    shouldDraw=True
    kubSetCheck.clear()
    playerId+=1
print('<GAMEOVER>\nWinner:',end='')
if stack==[]:
    print('Stack')
else:
    for i in playerStack:
        if i==[]:
            kubSetCheck.append(i)
            break
    print('Player#',kubSetCheck[0]+1,sep='')