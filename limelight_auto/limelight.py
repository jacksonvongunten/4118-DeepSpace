import limelight_auto.limelight_tx
import limelight_auto.limelight_ty
from networktables import NetworkTables
import wpilib.drive

dash = NetworkTables.getTable("dash")

class Limelight:

    def __init__(self, l_motor, r_motor):
        self.drive = wpilib.drive.DifferentialDrive(l_motor, r_motor)

    def drive(self):
        tx = dash.getNumber("tx")
        ty = dash.getNumber("ty")
        self.drive.arcadeDrive(tx,ty)
