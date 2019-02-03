import wpilib
from networktables import NetworkTables
import wpilib.drive
import ctre

class Robot(wpilib.TimedRobot):

	def robotInit(self):
		NetworkTables.initialize(server="10.41.18.2")

		self.l_motor = ctre.WPI_VictorSPX(1)
		self.l1_motor = ctre.WPI_VictorSPX(3)
		self.l2_motor = ctre.WPI_VictorSPX(6)

		self.l1_motor.set(ctre.ControlMode.Follower, 1)
		self.l2_motor.set(ctre.ControlMode.Follower, 1)

		self.r_motor = ctre.WPI_VictorSPX(0)
		self.r1_motor = ctre.WPI_VictorSPX(2)
		self.r2_motor = ctre.WPI_VictorSPX(4)

		self.r1_motor.set(ctre.ControlMode.Follower, 0)
		self.r2_motor.set(ctre.ControlMode.Follower, 0)

		self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)
		self.drive.setSafetyEnabled(False)

		self.elevator = ctre.WPI_TalonSRX(0)

		self.controller = wpilib.XboxController(0)

		self.dash = NetworkTables.getTable("dash")
		self.lime_table = NetworkTables.getTable("limelight")

		self.lime_table.putNumber("camMode", 1)
		self.lime_table.putNumber("ledMode", 1)

		self.led = 0b0

	def reset(self):
		self.drive.arcadeDrive(0.0, 0.0)

	def toggle(self):
		if self.controller.getAButtonPressed():
			if self.led == 0b0:
				self.lime_table.putNumber("camMode", 0)
				self.lime_table.putNumber("ledMode", 3)
				self.led = 0b1
			else:
				self.lime_table.putNumber("ledMode", 1)
				self.lime_table.putNumber("camMode", 1)
				self.led = 0b0

	def disabledInit(self):
		self.lime_table.putNumber("ledMode", 1)
		self.led = 0b1

	def disabledPeriodic(self):
		self.lime_table.putNumber("ledMode", 1)
		self.led = 0b1
	
	def autonomousInit(self):
		self.reset()
	
	def autonomousPeriodic(self):
		pass
	
	def align(self):
		error = self.lime_table.getNumber("tx", 0.0)
		minCommand = 0.35

		if abs(error) <= 3.0:
			output = 0
			self.drive.arcadeDrive(-self.controller.getRawAxis(1), 0.0)
		else:
			output = error/40.0
		
		if (output != 0 and abs(output) < minCommand):
			output = minCommand
			if error > 0:
				self.drive.curvatureDrive(-self.controller.getRawAxis(1), output, False)
			else:
				self.drive.curvatureDrive(-self.controller.getRawAxis(1), -output, False)
		else:
			self.drive.curvatureDrive(-self.controller.getRawAxis(1), output, False)

	def teleopInit(self):
		self.reset()

	def teleopPeriodic(self):
		self.toggle()

		if (self.controller.getXButton() and self.lime_table.getNumber("tv", 0)):
			self.align()

		if (not self.controller.getXButton()):
			forward = self.controller.getRawAxis(1)
			rotate = self.controller.getRawAxis(4)
			self.drive.curvatureDrive(-forward, rotate, False)

		if (self.controller.getRawAxis(3) > 0):
			self.elevator.set(self.controller.getRawAxis(3))
		elif (self.controller.getRawAxis(2) > 0):
			self.elevator.set(-self.controller.getRawAxis(2))
		else:
			self.elevator.set(0.0)

if __name__ == '__main__':
	wpilib.run(Robot)
