from config import Config
import feedparser

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
	
	def getTodos(self):
		d = feedparser.parse(self.url)
		return d.entries
