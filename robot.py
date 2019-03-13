import wpilib
from networktables import NetworkTables
import wpilib.drive
import ctre
import elevatorPID

class Robot(wpilib.TimedRobot):

	def robotInit(self):
		NetworkTables.initialize(server="10.41.18.2")

		self.left1 = ctre.WPI_VictorSPX(4)
		self.left2 = ctre.WPI_VictorSPX(3)
		self.left3 = ctre.WPI_VictorSPX(5)

		self.left2.set(ctre.ControlMode.Follower, 4)
		self.left3.set(ctre.ControlMode.Follower, 4)

		self.right1 = ctre.WPI_VictorSPX(0)
		self.right2 = ctre.WPI_VictorSPX(1)
		self.right3 = ctre.WPI_VictorSPX(2)

		self.right2.set(ctre.ControlMode.Follower, 0)
		self.right3.set(ctre.ControlMode.Follower, 0)

		self.drive = wpilib.drive.DifferentialDrive(self.left1, self.right1)
		self.drive.setSafetyEnabled(False)

		self.elevator = ctre.WPI_TalonSRX(0)

		self.controller = wpilib.XboxController(0)

		self.dash = NetworkTables.getTable("dash")
		self.lime_table = NetworkTables.getTable("limelight")

		self.lime_table.putNumber("camMode", 1)
		self.lime_table.putNumber("ledMode", 1)

		self.led = 0b0

		self.piston = wpilib.DoubleSolenoid(0, 1)

		self.limit = wpilib.DigitalInput(0)

		self.level2 = elevatorPID.elevatorPID(self.elevator, 340000, 2)
		self.level3 = elevatorPID.elevatorPID(self.elevator, 670000, 8)

		self.ultrasonic = wpilib.AnalogInput(0)

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

	def fire(self):
		if (self.controller.getXButton()) and (self.ultrasonic.getVoltage() < 0.3):
			self.piston.set(1)
		else:
			self.piston.set(2)

	def elevate(self):
		if (self.controller.getRawAxis(3) > 0):
			self.elevator.set(0.15*self.controller.getRawAxis(3))
		elif (self.controller.getRawAxis(2) > 0):
			self.elevator.set(-self.controller.getRawAxis(2))
		else:
			self.elevator.set(0.0)
	
	def seek(self):
		forward = -self.controller.getRawAxis(1)
		turn = 0.0167*self.lime_table.getNumber("tx", 0.0)

		if (abs(self.lime_table.getNumber("tx", 0.0)) > 2):
			self.drive.curvatureDrive(forward, turn, True)
		else:
			self.drive.curvatureDrive(forward, 0.0, False)
	
	def autonomousInit(self):
		self.drive.curvatureDrive(0.0, 0.0, False)
		self.lime_table.putNumber("camMode", 1)
	
	def autonomousPeriodic(self):

		forward = -self.controller.getRawAxis(1)
		turn = self.controller.getRawAxis(4)

		self.drive.curvatureDrive(forward, turn, False)		
		self.elevate()
		self.toggle()
		self.fire()

		if (not self.limit.get()):
			self.elevator.setQuadraturePosition(0)
		
		self.dash.putNumber("encoder", self.elevator.getQuadraturePosition())

		if self.controller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
			self.level2.execute()
	
	def teleopInit(self):
		self.drive.curvatureDrive(0.0, 0.0, False)
		self.lime_table.putNumber("camMode", 1)

	def teleopPeriodic(self):

		if (not self.controller.getBumper(wpilib.interfaces.GenericHID.Hand.kLeft)):
			forward = -self.controller.getRawAxis(1)
			turn = 0.7*self.controller.getRawAxis(4)

			self.drive.curvatureDrive(forward, turn, False)		
			self.elevate()
			self.toggle()
			self.fire()

			if (not self.limit.get()):
				self.elevator.setQuadraturePosition(0)

			if (self.controller.getBButton()):
				self.level2.execute()
			
			if (self.controller.getYButton()):
				self.level3.execute()
		
			self.dash.putNumber("encoder", self.elevator.getQuadraturePosition())

			if self.controller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
				self.level2.execute()
		else:
			self.seek()


if __name__ == '__main__':
	wpilib.run(Robot)
