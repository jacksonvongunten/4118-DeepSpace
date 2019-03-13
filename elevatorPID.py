import wpilib.drive
import math

class elevatorPID:

    def __init__(self, elevator, goal, p):
        self.elevator = elevator
        self.goal = goal
    
        self.P = p/self.goal
        self.I = 15.0/(self.goal**2)
        self.D = 2.0/(self.goal**2)

        self.integral = 0
        self.previousError = 0
        self.output = 0

    def PID(self):
        error = self.goal - self.elevator.getQuadraturePosition()
        self.integral += error*0.2
        derivative = (error - self.previousError) / 0.02
        self.output = self.P*error + self.I*self.integral + self.D*derivative
        self.previousError = error
    
    def execute(self):
        self.PID()
        self.elevator.set(-self.output)