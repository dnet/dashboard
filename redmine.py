from config import Config
import feedparser
import re

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
		self.title = re.compile(r'^(.* - .* #[0-9]+ \(.*\)): (.*)$')

	def explodeTitle(self, entry):
		match = self.title.match(entry.title)
		if match is not None:
			entry.title = match.group(2)
			entry.subtitle = match.group(1)
		return entry

	def getTodos(self):
		d = feedparser.parse(self.url)
		return map(self.explodeTitle, d.entries)
