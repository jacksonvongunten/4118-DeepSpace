import wpilib
from networktables import NetworkTables
import limelight
import wpilib.drive
import ctre

class Robot(wpilib.TimedRobot):

	def robotInit(self):
		self.lf_motor = ctre.WPI_VictorSPX(0)
		self.rf_motor = ctre.WPI_VictorSPX(1)
		self.lb_motor = ctre.WPI_VictorSPX(2)
		self.rb_motor = ctre.WPI_VictorSPX(3)

		self.lb_motor.set(ctre.ControlMode.Follower, 0)
		self.rb_motor.set(ctre.ControlMode.Follower, 1)

		self.drive = wpilib.drive.DifferentialDrive(self.lf_motor, self.rf_motor)

		NetworkTables.initialize(server="10.41.18.2")
		self.dash = NetworkTables.getTable("dash")

		self.auto_poster = [limelight.Limelight("tx"), limelight.Limelight("ty")]
	
	def update(self):
		for i in self.auto_poster:
			i.execute()

	def limelight(self):
		tx = self.dash.getNumber("tx", 0.0)
		ty = self.dash.getNumber("ty", 0.0)
		self.drive.arcadeDrive(ty, tx)
	
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
