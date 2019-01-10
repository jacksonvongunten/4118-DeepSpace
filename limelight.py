from networktables import NetworkTables
import math

class Limelight:

    def __init__(self, parameter):
        
        NetworkTables.initialize(server="10.41.18.2" )
        self.table = NetworkTables.getTable("limelight")
        self.dash = NetworkTables.getTable("dash")
        
        self.parameter = parameter
        self.setpoint = 0.0

        self.P = 1
        self.D = 0

        self.prev_error = 0

    def sigmoid(self, z):
        return 1/(1 + math.e**-z)

    def PID(self):
        error = -self.table.getNumber(self.parameter, 0.0)
        derivative = (error - self.prev_error) / 0.02
        raw_adjust = self.P*error + self.D*derivative
        self.adjust = self.sigmoid(raw_adjust)
        self.prev_error = error

    def execute(self):
        self.PID()
        self.dash.putNumber(self.parameter, self.adjust)
