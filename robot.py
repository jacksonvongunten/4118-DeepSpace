import wpilib
from networktables import NetworkTables
import limelight
import wpilib.drive
import ctre

class Robot(wpilib.TimedRobot):

	def robotInit(self):
		NetworkTables.initialize(server="10.41.18.2")

		self.l_motor = ctre.WPI_VictorSPX(7)
		self.l1_motor = ctre.WPI_VictorSPX(6)
		self.l2_motor = ctre.WPI_VictorSPX(5)

		self.l_motor.setInverted(True)
		self.l1_motor.set(ctre.ControlMode.Follower, 7)
		self.l2_motor.set(ctre.ControlMode.Follower, 7)

		self.r_motor = ctre.WPI_VictorSPX(4)
		self.r1_motor = ctre.WPI_VictorSPX(3)
		self.r2_motor = ctre.WPI_VictorSPX(2)

		self.r1_motor.set(ctre.ControlMode.Follower, 4)
		self.r2_motor.set(ctre.ControlMode.Follower, 4)

		self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)
		self.drive.setSafetyEnabled(False)

		self.controller = wpilib.XboxController(0)

		self.dash = NetworkTables.getTable("dash")
		self.lime_table = NetworkTables.getTable("limelight")

		self.led = 0b0

		self.lime = limelight.Limelight()

	def toggle(self):
		if self.controller.getAButtonPressed():
			if self.led == 0b0:
				self.lime_table.putNumber("ledMode", 3)
				self.led = 0b1
			else:
				self.lime_table.putNumber("ledMode", 1)
				self.led = 0b0
	
	def autonomousInit(self):
		pass
	
	def autonomousPeriodic(self):
		pass
	
	def teleopInit(self):
		pass
	
	def teleopPeriodic(self):
		self.toggle()

		forward = self.controller.getRawAxis(1)
		rotate = self.controller.getRawAxis(4)

		self.drive.arcadeDrive(-forward, rotate)

if __name__ == '__main__':
	wpilib.run(Robot)
