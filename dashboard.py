from __future__ import with_statement
from django.template import Template, Context
from django.conf import settings
from config import Config
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
	for todo in mlist:
		todo['src'] = cn
	return acc + mlist

cvals = loadcfg()
mods = [getattr(__import__(m), m.capitalize())() for m in cvals['modules'].split(',')]
todos = reduce(getTodos, mods, [])

tpl = None
settings.configure()
with open(cvals['template'], 'r') as f:
	tpl = Template(f.read())

html = tpl.render(Context({'todos': todos}))
with open(cvals['output'], 'w') as f:
	f.write(html.encode('utf-8'))
