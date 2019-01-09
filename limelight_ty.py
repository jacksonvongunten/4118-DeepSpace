from networktables import NetworkTables
import wpilib.drive
import math

limelight_table = NetworkTables.getTable("limelight")
dash = NetworkTables.getTable("dash")

class adjust_ty:
    
    def __init__(self):
        self.setpoint = 0.0
        
        self.P = 1
        self.D = 1

        self.prev_error = 0

        def sigmoid(z):
            return 1/(1 + math.e**-z)

        def PID(self):
            error = -limelight_table.getNumber("ty")
            self.derivative = (error - self.prev_error) / 0.02
            raw_adjust = self.P*error + self.D*derivative
            self.adjust = sigmoid(raw_adjust)
            self.prev_error = error
        
        def execute(self):
            self.PID()
            dash.putNumber("ty", self.adjust)
            