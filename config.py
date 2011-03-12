from PyQt4 import QtCore

class Config(QtCore.QSettings):
	def __init__(self):
		QtCore.QSettings.__init__(self, 'dnet', 'dashboard')
