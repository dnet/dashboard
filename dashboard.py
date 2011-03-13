from __future__ import with_statement
from django.template import Template, Context
from django.conf import settings
from config import Config
import datetime
import sys
import os

def loadcfg():
	cfg = Config()
	ckeys = ['modules', 'output', 'template']
	cvals = dict()
	for key in ckeys:
		cvals[key] = str(cfg.value('core/' + key).toString())
		if cvals[key] == '':
			print 'Key %s is not configured, check your configuration!' % key
			sys.exit(1)
	return cvals

def getTodos(acc, module):
	mlist = module.getTodos()
	cn = module.__class__.__name__
	noon = datetime.time(12)
	now = datetime.datetime.now()
	dl = datetime.datetime.now() + datetime.timedelta(weeks = 10)
	for todo in mlist:
		todo['src'] = cn
		if 'deadline' not in todo:
			todo['deadline_cmp'] = dl
		elif type(todo['deadline']) == datetime.date:
			todo['deadline_cmp'] = datetime.datetime.combine(todo['deadline'], noon)
		elif type(todo['deadline']) != datetime.datetime:
			todo['deadline_cmp'] = dl
		else:
			todo['deadline_cmp'] = todo['deadline']
		todo['late'] = todo['deadline_cmp'] < now
	return acc + mlist

cvals = loadcfg()
mods = [getattr(__import__(m), m.capitalize())() for m in cvals['modules'].split(',')]
todos = reduce(getTodos, mods, [])
todos.sort(lambda x, y: cmp(x['deadline_cmp'], y['deadline_cmp']))

tpl = None
settings.configure()
with open(cvals['template'], 'r') as f:
	tpl = Template(f.read())

html = tpl.render(Context({'todos': todos}))
with open(cvals['output'], 'w') as f:
	f.write(html.encode('utf-8'))
