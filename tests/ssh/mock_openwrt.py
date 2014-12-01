
import MockSSH

class command_cat(MockSSH.SSHCommand):
	"""
	mock output of `cat /proc/meminfo | grep MemTotal | awk '{print $2}'`
	"""
	name = 'cat'

	def start(self):
		self.writeln("32854")
		self.exit()


commands = [command_cat]
