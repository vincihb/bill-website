class HMException(Exception):
	def __init__(self, message='Server Error'):
		self.message = message


class HMBillException(HMException):
	def __init__(self, message='Bill I/O Error'):
		self.message = message

class CCException(HMException):
	def __init__(self, message='CongressCache I/O Error'):
		self.message = message