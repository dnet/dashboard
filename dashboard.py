from config import Config

modnames = str(Config().value('core/modules').toString())
mods = [getattr(__import__(m), m.capitalize())() for m in modnames.split(',')]
todos = reduce(lambda a, e: a + e.getTodos(), mods, [])

for todo in todos:
	print todo['title']
