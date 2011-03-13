from config import Config
import sys

modnames = str(Config().value('core/modules').toString())
if modnames == '':
	print 'No modules are configured, check your configuration!'
	sys.exit(1)

mods = [getattr(__import__(m), m.capitalize())() for m in modnames.split(',')]
todos = reduce(lambda a, e: a + e.getTodos(), mods, [])

for todo in todos:
	print todo['title']
	print "\t", todo['subtitle']
