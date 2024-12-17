"""corriere controller."""

#Classe Graph che trasforma la mappa in un grafo e permette di usare l'algoritmo a*
class Graph:

    def __init__(self, map):

        graph={}
        for i in range(16):
            graph[i]=[]
            if map[i][0]!=0:
                continue
            if map[i][1]==0:
                graph[i].append(i-4)
            if map[i][2]==0:
                graph[i].append(i+1)
            if map[i][3]==0:
                graph[i].append(i+4)
            if map[i][4]==0:
                graph[i].append(i-1)

        self.graph=graph
    
    def get_neighbors(self, n):
        return self.graph[n]
 
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start 
        #node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + 1 < poo[n] + 1:
                    n = v;
 
            if n == None:
                return None
 
            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []
 
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
 
                reconst_path.append(start)
 
                reconst_path.reverse()

                #print(reconst_path)
                return reconst_path
 
            # for all the neighbors of the current node do
            for m in self.get_neighbors(n):
              # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + 1
 
                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + 1:
                        poo[m] = poo[n] + 1
                        par[m] = n
 
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)
 
            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        return None
    
    
from controller import Robot, Emitter, Receiver

#Istanze del robot, emettitore e ricevitore
robot = Robot()
emitter=Emitter('emitter')
receiver=Receiver('receiver')

#Dati sul robot
raggio=111/1000     #raggio ruote
asse=381/1000       #distanza tra ruote 
dir='N'             #direzione
start=12            #posizione iniziale
pos=start           #posizione
emote='normale'     #stato emozionale

mappa=[[0,1,1,0,1],['R',1,0,0,0],[0,1,0,0,1],[0,1,1,0,0],
       ['G',0,0,0,1],[0,1,0,0,1],[0,0,0,0,0],[0,0,1,1,0],
       [0,1,0,0,1],[0,0,0,0,0],[0,0,1,0,0],['B',0,1,0,0],
       [0,0,0,1,1],[0,0,0,1,0],[0,0,0,1,0],[0,1,1,1,0]]

#Istanza del grafo a partire dalla mappa
grafo=Graph(mappa)

#Timestep del mondo corrente
timestep = int(robot.getBasicTimeStep())

#Istanza delle variabili dei motori delle ruote
b_sx = robot.getDevice('back left wheel')
b_dx = robot.getDevice('back right wheel')
f_sx = robot.getDevice('front left wheel')
f_dx = robot.getDevice('front right wheel')
b_sx.setPosition(float('inf'))
b_dx.setPosition(float('inf'))
f_sx.setPosition(float('inf'))
f_dx.setPosition(float('inf'))
b_sx.setVelocity(0)
b_dx.setVelocity(0)
f_sx.setVelocity(0)
f_dx.setVelocity(0)

#Istanza del motore del piano di appoggio
m=robot.getDevice('motor')
m.setPosition(float('inf'))
m.setVelocity(0)

#Il robot avanza in avanti di una cella
def move_forward():
    if emote=='felice':
        speed=6.28
    else:
        speed=3.14
    speed_ms=speed*raggio
    time=0.75/speed_ms + robot.getTime()
    b_sx.setVelocity(speed)
    b_dx.setVelocity(speed)
    f_sx.setVelocity(speed)
    f_dx.setVelocity(speed)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            b_sx.setVelocity(0)
            b_dx.setVelocity(0)
            f_sx.setVelocity(0)
            f_dx.setVelocity(0)
            break

#Il robot ruota nel verso indicato
#1: senso orario
#-1: senso antiorario
def rotate(verso):
    spazio=5*asse/4
    speed=3.14
    speed_ms=speed*raggio
    time=spazio/speed_ms + robot.getTime()
    b_sx.setVelocity(speed*verso)
    b_dx.setVelocity(speed*verso*-1)
    f_sx.setVelocity(speed*verso)
    f_dx.setVelocity(speed*verso*-1)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            b_sx.setVelocity(0)
            b_dx.setVelocity(0)
            f_sx.setVelocity(0)
            f_dx.setVelocity(0)
            break

#Il robot punta a Nord
def face_nord():
    global dir

    if dir=='S':
        rotate(1)
        rotate(1)
    if dir=='E':
        rotate(-1)
    if dir=='O':
        rotate(1)

    dir='N'
    return

#Il robot punta a Sud
def face_sud():
    global dir

    if dir=='E':
        rotate(1)
    if dir=='N':
        rotate(1)
        rotate(1)
    if dir=='O':
        rotate(-1)

    dir='S'
    return

#Il robot punta a Est
def face_est():
    global dir

    if dir=='S':
        rotate(-1)
    if dir=='O':
        rotate(1)
        rotate(1)
    if dir=='N':
        rotate(1)
    dir='E'

    return

#Il robot punta a Ovest
def face_ovest():
    global dir

    if dir=='S':
        rotate(1)
    if dir=='E':
        rotate(1)
        rotate(1)
    if dir=='N':
        rotate(-1)
    dir='O'
    return

#Il robot si mette in attesa per mezzo secondo
def wait():
    time=0.5 + robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            break

#Il robot segue il percorso, cioè la sequenza di celle restituite da a*
def follow_path(path):

    global pos
    for i in range(1,len(path)):
        next=path[i]
        if next==pos+1:
            face_est()
        if next==pos-1:
            face_ovest()
        if next==pos+4:
            face_sud()
        if next==pos-4:
            face_nord()

        move_forward()
        pos=path[i]
    
    return

#Viene azionato il motore del piano di appoggio
def scarica():
    arco = 60/360   
    time= robot.getTime() + arco
    m.setVelocity(-6.28)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            m.setVelocity(0)
            break
    wait()
    wait()
    time=robot.getTime() + arco
    m.setVelocity(6.28)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            m.setVelocity(0)
            return

#Viene ricevuto il messaggio contenente la destinazione
def get_destinazione():
    message=''
    while robot.step(timestep) != -1:
        while receiver.getQueueLength() >0:
            message=receiver.getString()
            receiver.nextPacket()
        
        if message!='':
            return message

#Viene calcolata la cella in cui si trova la casa di destinazione    
def get_pos_casa(dest):
    for i in range(len(mappa)):
        if mappa[i][0]==dest:
            return i

#Il robot manda un messaggio di sincronizzazione
def send_OK():
    emitter.send("OK")

#Esecuzione
send_OK() #Il robot segnala di essere pronto per l'esecuzione
dest=get_destinazione()
while dest!='OK':                          #Finché ci sono consegne da effettuare
    c=get_pos_casa(dest)
    path=grafo.a_star_algorithm(pos,c+4)   #Viene calcolato il percorso per la cella sottostante alla destinazione
    follow_path(path)
    face_sud()
    scarica()
    emote='felice'                         #Il robot cambia il suo stato emozionale in seguito alla consegna effettuata
    send_OK()                              #Viene segnalata l'avvenuta consegna
    path=grafo.a_star_algorithm(pos,start) #Il robot torna alla posizione iniziale
    follow_path(path)
    face_nord()
    send_OK()                              #Il robot è pronto per una nuova consegna
    emote='normale'
    dest=get_destinazione()