import wpilib
from networktables import NetworkTables
import limelight
import wpilib.drive
import ctre

class Robot(wpilib.TimedRobot):

	def robotInit(self):
		NetworkTables.initialize(server="10.41.18.2")

		self.lf_motor = ctre.WPI_VictorSPX(0)
		self.rf_motor = ctre.WPI_VictorSPX(1)
		self.lb_motor = ctre.WPI_VictorSPX(2)
		self.rb_motor = ctre.WPI_VictorSPX(3)

		self.lb_motor.set(ctre.ControlMode.Follower, 0)
		self.rb_motor.set(ctre.ControlMode.Follower, 1)

		self.drive = wpilib.drive.DifferentialDrive(self.lf_motor, self.rf_motor)

		self.dash = NetworkTables.getTable("dash")

		self.lime = limelight.Limelight()
	
	def update(self):
		self.lime.execute()

	def align(self):
		tx = self.dash.getNumber("tx", 0.0)
		self.drive.arcadeDrive(0.7, tx)
	
	def autonomousInit(self):
		self.update()
	
	def autonomousPeriodic(self):
		self.update()
	
	def teleopInit(self):
		self.update()
	
	def teleopPeriodic(self):
		self.update()

if __name__ == '__main__':
	wpilib.run(Robot)
