import Orgnode
import os
from config import Config

class Orgmode:
	def __init__(self):
		self.dir = unicode(Config().value('orgmode/dir').toString())
		if not os.path.isdir(self.dir):
			raise Exception('Org-mode directory is invalid or empty')

	def subtitle(self, parents):
		return '/'.join(map(Orgnode.Orgnode.Heading, parents))

	def getTodos(self):
		ls = filter(lambda x: x.endswith('.org'), os.listdir(self.dir))
		result = list()
		for f in ls:
			fn = os.path.join(self.dir, f)
			nodes = Orgnode.makelist(fn)
			parents = list()
			for node in nodes:
				lvl = node.Level()
				while len(parents) >= lvl:
					parents.pop()
				if node.Todo() == 'TODO':
					result.append({'title': node.Heading(), 'deadline': node.Deadline(),
						'link': 'file://' + fn, 'subtitle': self.subtitle(parents)})
				parents.append(node)
		return result
