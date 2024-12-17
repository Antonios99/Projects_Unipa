import numpy as np

#Classe Kalman Filter che contiene i metodi update e predict per applicare il filtro di Kalman
class KalmanFilter(object):
    def __init__(self, dt, u_x,u_y, std_acc, x_std_meas, y_std_meas):
        """
        :param dt: sampling time (time for 1 cycle)
        :param u_x: acceleration in x-direction
        :param u_y: acceleration in y-direction
        :param std_acc: process noise magnitude
        :param x_std_meas: standard deviation of the measurement in x-direction
        :param y_std_meas: standard deviation of the measurement in y-direction
        """

        # Define sampling time
        self.dt = dt

        # Define the  control input variables
        self.u = np.matrix([[u_x],[u_y]])

        # Intial State
        self.x = np.matrix([[0], [0], [0], [0]])

        # Define the State Transition Matrix A
        self.A = np.matrix([[1, 0, self.dt, 0],
                            [0, 1, 0, self.dt],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        # Define the Control Input Matrix B
        self.B = np.matrix([[(self.dt**2)/2, 0],
                            [0, (self.dt**2)/2],
                            [self.dt,0],
                            [0,self.dt]])

        # Define Measurement Mapping Matrix
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        #Initial Process Noise Covariance
        self.Q = np.matrix([[(self.dt**4)/4, 0, (self.dt**3)/2, 0],
                            [0, (self.dt**4)/4, 0, (self.dt**3)/2],
                            [(self.dt**3)/2, 0, self.dt**2, 0],
                            [0, (self.dt**3)/2, 0, self.dt**2]]) * std_acc**2

        #Initial Measurement Noise Covariance
        self.R = np.matrix([[x_std_meas**2,0],
                           [0, y_std_meas**2]])

        #Initial Covariance Matrix
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        # Refer to :Eq.(9) and Eq.(10)  in https://machinelearningspace.com/object-tracking-simple-implementation-of-kalman-filter-in-python/?preview_id=1364&preview_nonce=52f6f1262e&preview=true&_thumbnail_id=1795

        # Update time state
        #x_k =Ax_(k-1) + Bu_(k-1)     Eq.(9)
        self.x = np.dot(self.A, self.x) + np.dot(self.B, self.u)

        # Calculate error covariance
        # P= A*P*A' + Q               Eq.(10)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]
    
    def update(self, z):

        # Refer to :Eq.(11), Eq.(12) and Eq.(13)  in https://machinelearningspace.com/object-tracking-simple-implementation-of-kalman-filter-in-python/?preview_id=1364&preview_nonce=52f6f1262e&preview=true&_thumbnail_id=1795
        # S = H*P*H'+R
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R

        # Calculate the Kalman Gain
        # K = P * H'* inv(H*P*H'+R)
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  #Eq.(11)

        self.x =self.x + np.dot(K, (z - np.dot(self.H, self.x)))  #Eq.(12)

        I = np.eye(self.H.shape[1])

        # Update error covariance matrix
        self.P = (I - (K * self.H)) * self.P   #Eq.(13)
        return self.x[0:2]

from controller import Robot

#Istanza del robot
robot = Robot()

#Memorizzazione delle posizioni delle case
positions={
    'R':0,
    'G':0,
    'B':0
}

#Dati del robot
speed=3.14                  #velocità di movimento in rad/s
raggio=111/1000             #raggio delle ruote
speed_ms=speed*raggio       #velocità di movimento in m/s
asse=381/1000               #distanza tra le ruote
dir='N'                     #direzione
pos=12                      #posizione

#Timestep del mondo corrente
timestep = int(robot.getBasicTimeStep())

#Istanza dell'oggetto KF
#KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)
KF = KalmanFilter(0.001*timestep, 0, 0, 1, 0.1,0.1)

#Istanza delle variabili dei sensori di distanza
ds0 = robot.getDevice('ds0')
ds1 = robot.getDevice('ds1')
ds2 = robot.getDevice('ds2')
ds3 = robot.getDevice('ds3')
dw0 = robot.getDevice('dw0')
dw1 = robot.getDevice('dw1')
ds0.enable(timestep)
ds1.enable(timestep)
ds2.enable(timestep)
ds3.enable(timestep)
dw0.enable(timestep)
dw1.enable(timestep)

#Istanza della variabile della camera
camera = robot.getDevice('camera')
camera.enable(timestep)
camera.recognitionEnable(timestep)

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

#Il robot ruota nel verso indicato
#1: senso orario
#-1: senso antiorario
def rotate(verso):
    spazio=5.1*asse/4
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

#Vengono letti i dati dei due sensori, uno per la x e uno per la y
#a seconda della direzione
def get_ds_sesnor():
    global dir

    if dir=='N':
        return np.array([[ds0.getValue()], [ds3.getValue()]])
    
    if dir=='S':
        return np.array([[ds2.getValue()], [ds1.getValue()]])
    
    if dir=='E':
        return np.array([[ds3.getValue()], [ds2.getValue()]])
    
    if dir=='O':
        return np.array([[ds1.getValue()], [ds0.getValue()]])

#Viene ricavata la posizione del robot usando il filtro di Kalman
def get_position(): 
    # Ottieni le letture dei sensori
    measurement = get_ds_sesnor()
    # Predici lo stato usando il filtro di Kalman
    KF.predict()
    # Aggiorna lo stato usando la misura dei sensori
    return KF.update(measurement)

#Viene mappata la posizione in coordinate x y nel numero della cella corrispondente
def get_cell(x,y):
    a=int(x//0.75)
    b=int(y//0.75)

    if a>3:
        a=3

    if b>3:
        b=3

    l=[12,8,4,0]

    return l[b]+a

#Se viene rilevato un oggetto, ne viene ricavato il colore attraverso la camera
def check_colore():
    obj=camera.getRecognitionObjects()
    if obj:
        colore = obj[0].getColors()
        if colore[0]==1.0 and colore[1]==0 and colore[2]==0:
            return 'R'
        if colore[0]==0 and colore[1]==0 and colore[2]==1:
            return 'B'
        if colore[0]==1.0 and colore[1]==1.0 and colore[2]==0:
            return 'G'
    return False

#Viene memorizzata la posizione delle case a seconda del colore e della direzione
def save_pos(colore):
    if dir=='N':
        positions[colore]=pos-4
    if dir=='S':
        positions[colore]=pos+4
    if dir=='E':
        positions[colore]=pos+1
    if dir=='O':
        positions[colore]=pos-1

#Verifica se il robot dovrebbe fermarsi
#Quindi controlla se è stata memorizzata la posizione di tutte le case
def check_stop():
    for k in positions.keys():
        if positions[k]==0:
            return False
    return True

#Controlla se il robot deve ruotare seguendo la logica del wall-follow
def check_turn():
    if dw0.getValue()>=0.4 and dw1.getValue()>=0.4:
        return -1
    if dw0.getValue()<0.4:
        return 1
    
    return False

#Aggiorna la direzione del robot a seconda del verso con cui ha ruotato
def change_dir(turn):
    global dir
    if dir=='N':
        if turn==1:
            dir='E'
        else:
            dir='O'
        return 
    
    if dir=='S':
        if turn==1:
            dir='O'
        else:
            dir='E'
        return
    
    if dir=='E':
        if turn==1:
            dir='S'
        else:
            dir='N'
        return
    
    if dir=='O':
        if turn==1:
            dir='N'
        else:
            dir='S'
        return

#Esecuzione
while True:
    time=0.75/speed_ms + robot.getTime()    #Viene calcolato per quanto tempo il robot deve azionare
                                            #i motori delle ruote per avanzare di una cella
    while robot.step(timestep)!=-1:

        b_sx.setVelocity(3.14)
        b_dx.setVelocity(3.14)
        f_sx.setVelocity(3.14)
        f_dx.setVelocity(3.14)

        (x,y) = get_position()
        c = get_cell(x[0],y[0])
        pos = c                                 #Viene aggiornata la posizione del robot

        colore=check_colore()
        if dw0.getValue() <= 0.4 and colore:    #Se l'oggetto è abbastanza vicino e rispecchia uno dei colori
            save_pos(colore)                    #ne viene memorizzata la posizione

        if robot.getTime()>=time:               #Il robot è avanzato di una cella e si ferma
            b_sx.setVelocity(0)
            b_dx.setVelocity(0)
            f_sx.setVelocity(0)
            f_dx.setVelocity(0)
            break
    
    if check_stop():
        break

    turn=check_turn()
    if turn:
        rotate(turn)
        change_dir(turn) 

#Vengono visualizzate le posizioni rilevate delle case
print(f'Casa Rossa rilevata nella cella: {positions["R"]}')
print(f'Casa Blu rilevata nella cella: {positions["B"]}')
print(f'Casa Gialla rilevata nella cella: {positions["G"]}')