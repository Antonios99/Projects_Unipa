"""presa controller."""

from controller import Robot, Emitter, Receiver

#Istanze del robot, emettitore e ricevitor
robot = Robot()
emitter=Emitter('emitter')
receiver=Receiver('receiver')

#Dati sul robot
consegne=["R", "G", "B"]    #Lista consegne da effettuare
speed=3.14                  #Velocità di movimento in rad/s
raggio=0.05                 #Raggio delle ruote
speed_ms=speed*raggio       #Velocità di movimento in m/s
pos=0

#Timestep del mondo corrente
timestep = int(robot.getBasicTimeStep())

#Istanza delle variabili dei motori delle ruote
r_sx = robot.getDevice('rear left')
r_dx = robot.getDevice('rear right')
f_sx = robot.getDevice('front left')
f_dx = robot.getDevice('front right')
r_sx.setPosition(float('inf'))
r_dx.setPosition(float('inf'))
f_sx.setPosition(float('inf'))
f_dx.setPosition(float('inf'))
r_sx.setVelocity(0)
r_dx.setVelocity(0)
f_sx.setVelocity(0)
f_dx.setVelocity(0)

#Istanza dei motori dei bracci e della base
h=robot.getDevice('horizontal')
v=robot.getDevice('vertical')
l=robot.getDevice('left hand')
r=robot.getDevice('right hand')
b=robot.getDevice('base')
b.setPosition(float('inf'))
b.setVelocity(0)

#Il robot si mette in attesa per mezzo secondo
def wait():
    time=0.5 + robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            break

#Il robot aziona i bracci per prendere una scatola
def prendi():
    h.setPosition(0.3)
    l.setPosition(-0.18)
    r.setPosition(0.18)
    wait()
    v.setPosition(0.46)
    wait()
    r.setPosition(0.08)
    l.setPosition(-0.08)
    wait()
    v.setPosition(0)
    h.setPosition(0)

#Viene azionato il motore della base
def gira(verso=1):
    time=3/2 + robot.getTime()
    b.setVelocity(speed/3*verso)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            b.setVelocity(0)
            break

#Il robot aziona i bracci per rilasciare la scatola
def rilascia():
    h.setPosition(0.3)
    wait()
    l.setPosition(-0.18)
    r.setPosition(0.18)
    wait()
    h.setPosition(0)
    wait()
    l.setPosition(0)
    r.setPosition(0)

#Il robot avanza di una cella nel verso indicato
#1: in avanti
#-1: indietro
def sposta(dir):
    global pos
    time=0.75/speed_ms + robot.getTime()
    r_sx.setVelocity(speed*dir)
    r_dx.setVelocity(speed*dir)
    f_sx.setVelocity(speed*dir)
    f_dx.setVelocity(speed*dir)
    while robot.step(timestep) != -1:
        if robot.getTime()>=time:
            r_sx.setVelocity(0)
            r_dx.setVelocity(0)
            f_sx.setVelocity(0)
            f_dx.setVelocity(0)
            break
    pos+=dir

#Viene ricevuto il messagggio di sincronizzazione
def check():
    message=''
    while robot.step(timestep) != -1:
        while receiver.getQueueLength() >0:
            message=receiver.getString()
            receiver.nextPacket()
        
        if message=="OK":
            return

#Il robot manda un messaggio contenente la destinazione
def send(messaggio):
    emitter.send(messaggio)

#Il robot torna alla posizione iniziale
def pos_iniziale():
    for j in range(0,pos):
        sposta(-1)

#Esecuzione
for i in range(len(consegne)):  #Finché il magazzino non si svuota

    for k in range(0,i):        #Il robot raggiunge la cella antecedente la scatola
        sposta(1)

    gira(-1)
    wait()
    prendi()
    wait()
    gira(1)
    pos_iniziale()
    check()                     #Il robot aspetta che il corriere sia pronto per la consegna
    gira(1)
    wait()
    rilascia()
    send(consegne[i])
    gira(-1)
    check()                     #Il robot aspetta che la consegna sia avvenuta per prendere la scatola successiva

send("OK")                      #Il robot segnala che il magazzino è vuoto