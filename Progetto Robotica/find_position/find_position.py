from controller import Robot

TIME_STEP = 64
robot = Robot()
ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)

motor = []
MotorNames = ['motor_1', 'motor_2', 'motor_3', 'motor_4']
for i in range(4):
    motor.append(robot.getDevice(MotorNames[i]))
    motor[i].setPosition(float('inf'))
    motor[i].setVelocity(0.0)
avoidObstacleCounter = 0

rib = robot.getDevice('Piano')
rib.setPosition(float('inf'))
rib.setVelocity(0.0)
ribChangeDirectionTime = robot.getTime()

camera = robot.getDevice('camera')
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    leftSpeed = 5.0
    rightSpeed = 5.0

   
    if robot.getTime() - ribChangeDirectionTime > 5.0:
        leftSpeed *= -1
        rightSpeed *= -1
        ribChangeDirectionTime = robot.getTime()  

    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 5.0
        rightSpeed = -5.0
        
        camera_data = camera.getImage()
        
        estimated_position = (0.0, 0.0, 0.0)  
        print(f"ostacolo trovato, posizione robot: {estimated_position}")
    else:  # read sensors
        for i in range(2):
            if ds[i].getValue() < 950.0:
                avoidObstacleCounter = 100

    motor[0].setVelocity(leftSpeed)
    motor[1].setVelocity(rightSpeed)
    motor[2].setVelocity(leftSpeed)
    motor[3].setVelocity(rightSpeed)
    rib.setVelocity(0.0)  