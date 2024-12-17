from controller import Robot, Camera

TIME_STEP = 64
robot = Robot()

# Setup for obstacle avoidance
ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)

motor_obstacle_avoidance = []
MotorNames = ['motor_1', 'motor_2', 'motor_3', 'motor_4']
for i in range(4):
    motor_obstacle_avoidance.append(robot.getDevice(MotorNames[i]))
    motor_obstacle_avoidance[i].setPosition(float('inf'))
    motor_obstacle_avoidance[i].setVelocity(0.0)

rotate_speed = 10.0
search_speed = 5.0

# Camera setup
camera = robot.getDevice('camera')
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

avoidObstacleCounter = 0

while robot.step(TIME_STEP) != -1:
    # Obstacle avoidance logic
    leftSpeed = 5.0
    rightSpeed = 5.0

    for i in range(2):
        if ds[i].getValue() < 950.0:
            avoidObstacleCounter = 100
            leftSpeed = -5.0
            rightSpeed = -5.0

    motor_obstacle_avoidance[0].setVelocity(leftSpeed)
    motor_obstacle_avoidance[1].setVelocity(rightSpeed)
    motor_obstacle_avoidance[2].setVelocity(leftSpeed)
    motor_obstacle_avoidance[3].setVelocity(rightSpeed)

    # Color-based movement logic
    oggetti = camera.getRecognitionObjects()

    if oggetti:
        for oggetto in oggetti:
            colore_oggetto = oggetto.getColors()
            print(f"Valori colore oggetto: R={colore_oggetto[0]}, G={colore_oggetto[1]}, B={colore_oggetto[2]}")

    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
    else:
        for i in range(4):
            motor_obstacle_avoidance[i].setVelocity(-rotate_speed if i % 2 == 0 else rotate_speed)
