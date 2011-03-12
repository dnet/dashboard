import Orgnode
import os
from config import Config

class Orgmode:
	def __init__(self):
		self.dir = unicode(Config().value('orgmode/dir').toString())
	
	def getTodos(self):
		ls = filter(lambda x: x.endswith('.org'), os.listdir(self.dir))
		result = list()
		for f in ls:
			fn = os.path.join(self.dir, f)
			nodes = Orgnode.makelist(fn)
			for node in nodes:
				if node.Todo() != 'TODO':
					continue
				result.append({'title': node.Heading(), 'deadline': node.Deadline(),
					'link': 'file://' + fn})
		return result
