from serial import Serial

class MKS640(object):

	def __init__(self, address="/dev/mks640", timeout=1):
		self.name = "MKS640"
		self.dev = Serial(address, timeout=timeout)
		self.write_term = "\r\n"
		self.read_term = b"\r\n"
		self.max_pressure = 100.0

	def units(self):
		return (1.0, 'Torr')

	def write(self, cmd):
		self.dev.write((cmd + self.write_term).encode("utf-8"))

	def read(self):
		resp = self.dev.read_until(self.read_term)
		if len(resp)>=len(self.read_term) and resp[-2:]==self.read_term:
			return resp[:-2].decode("utf-8")
		else:
			raise TimeoutError("Read <%s>, expected <%s> termination." % (resp, self.read_term))

	def query(self, cmd):
		self.write(cmd)
		return self.read()

	def set_pressure(self, val):
		val = int(val / self.max_pressure * 4096)
		assert self.query("!SP %d" % val)[:3] == "SP="

	def get_pressure(self):
		resp = self.query("!GP")
		assert resp[:3] == "GP="
		return int(resp[3:]) * self.max_pressure / 1024

	def control_pressure(self, val=None):
		if val: self.set_pressure(val)
		assert self.query("!CP") == "PC"

	def open_valve(self):
		assert self.query("!OV") == "VO"

	def close_valve(self):
		assert self.query("!CV") == "VC"

	def test_valve(self):
		resp = self.query("!TV")
		assert resp[:3] == "TV="
		return bool(int(resp[3]))

	def test_trip(self, val="A"):
		resp = self.query("!TP" + val)
		assert resp[:4] == "TP" + val + "="
		return bool(int(resp[4]))