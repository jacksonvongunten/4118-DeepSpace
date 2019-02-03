import math
import wpilib
from networktables import NetworkTables

NetworkTables.initialize(server="10.41.18.2")

class AlignToTarget:

    def __init__(self, drive, controller):

        self.lime_table = NetworkTables.getTable("limelight")

        self.goal = self.lime_table.getNumber("tx", 0.0)
        self.drive = drive
        self.controller = wpilib.XboxController(0)

        try:
            self.P = 0.7/self.goal
            self.D = 1.0/(4*self.goal**2)
        except ZeroDivisionError:
            self.P = 0.0
            self.D = 0.0

        self.previous_error = 0.0
        self.output = 0.0

    def PID(self):
        error = self.goal - self.lime_table.getNumber("tx", 0.0)
        derivative = (error-self.previous_error)/0.02
        self.output = (self.P*error) + (self.D*derivative)
        self.previous_error = error
    
    def execute(self):
        self.PID()
        if abs(self.output < 0.1):
            return None
        else:
            if self.goal > 0:
                self.drive.arcadeDrive(-self.controller.getRawAxis(1), self.output)
            else:
                self.drive.arcadeDrive(-self.controller.getRawAxis(1), -self.output)
