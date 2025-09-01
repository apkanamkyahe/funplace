from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

hub = PrimeHub()
left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right = Motor(Port.E)

WHEEL_CIRCUMFERENCE_IN = 10.86614

def move(distance_in, speed=300, kp=3, ki=0.05, kd=0.4, tolerance=5):
    degrees_to_run = (distance_in / WHEEL_CIRCUMFERENCE_IN) * 360
    hub.imu.reset_heading(0)
    left.reset_angle(0)
    right.reset_angle(0)

    integral = 0
    last_error = 0

    while True:
        avg_degrees = (abs(left.angle()) + abs(right.angle())) / 2
        if avg_degrees >= degrees_to_run - tolerance:
            break

        error = hub.imu.heading()

        if abs(error) < 10:
            integral += error
            integral = max(min(integral, 100), -100)

        derivative = error - last_error
        correction = kp * error + ki * integral + kd * derivative

        remaining = degrees_to_run - avg_degrees
        if remaining < 50:
            speed_adj = max(100, int(speed * (remaining / 50)))
        else:
            speed_adj = speed

        left.run(speed_adj - correction)
        right.run(speed_adj + correction)

        last_error = error
        wait(10)

    left.hold()
    right.hold()

def move_backwards(distance_in, speed=300, kp=3, ki=0.05, kd=0.4, tolerance=5):
    degrees_to_run = (distance_in / WHEEL_CIRCUMFERENCE_IN) * 360
    hub.imu.reset_heading(0)
    left.reset_angle(0)
    right.reset_angle(0)

    integral = 0
    last_error = 0

    while True:
        avg_degrees = (abs(left.angle()) + abs(right.angle())) / 2
        if avg_degrees >= degrees_to_run - tolerance:
            break

        error = hub.imu.heading()

        if abs(error) < 10:
            integral += error
            integral = max(min(integral, 100), -100)

        derivative = error - last_error
        correction = kp * error + ki * integral + kd * derivative

        remaining = degrees_to_run - avg_degrees
        if remaining < 50:
            speed_adj = max(100, int(speed * (remaining / 50)))
        else:
            speed_adj = speed

        # Flip direction for backwards AND flip correction
        left.run(-(speed_adj + correction))
        right.run(-(speed_adj - correction))

        last_error = error
        wait(10)

    left.hold()
    right.hold()



def turn(target_angle, speed=400, kp=4.5, ki=0.03, kd=0.6, tolerance=2):
    hub.imu.reset_heading(0)
    integral = 0
    last_error = 0

    while True:
        error = target_angle - hub.imu.heading()
        if abs(error) <= tolerance:
            break

        if abs(error) < 15:
            integral += error
            integral = max(min(integral, 200), -200)

        derivative = error - last_error
        correction = kp * error + ki * integral + kd * derivative
        correction = max(min(correction, speed), -speed)

        left.run(correction)
        right.run(-correction)

        last_error = error
        wait(10)

    left.hold()
    right.hold()
