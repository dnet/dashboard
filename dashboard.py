#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# dashboard.py - generates an HTML file from modules using django
#
# Copyright (c) 2011 András Veres-Szentkirályi
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import with_statement
from itertools import imap, chain
from operator import itemgetter
from hashlib import sha1
from config import Config
import datetime
import sys
import os

def loadcfg():
	cfg = Config()
	ckeys = ['modules', 'output', 'template', 'thash']
	cvals = dict()
	for key in ckeys:
		cvals[key] = str(cfg.value('core/' + key).toString())
		if cvals[key] == '' and key != 'thash':
			print 'Key %s is not configured, check your configuration!' % key
			sys.exit(1)
	return cvals

def ensureDateTime(value, default, deftime):
	if type(value) == datetime.date:
		return datetime.datetime.combine(value, deftime)
	elif type(value) != datetime.datetime:
		return default
	else:
		return value

def getTodos(module):
	mlist = module.getTodos()
	cn = module.__class__.__name__
	noon = datetime.time(12)
	now = datetime.datetime.now()
	dl = datetime.datetime.now() + datetime.timedelta(weeks = 10)
	for todo in mlist:
		todo['src'] = cn
		todo['deadline_cmp'] = reduce(
			lambda default, field: ensureDateTime(todo.get(field, default), default, noon),
			['scheduled', 'deadline'], dl)
		todo['late'] = todo['deadline_cmp'] < now
		yield todo

def serializeTodo(todo):
	return '\t'.join('%s:%s' % i for i in sorted(todo.iteritems()) if i[0] != 'deadline_cmp')

cvals = loadcfg()
mods = [getattr(__import__(m), m.capitalize())() for m in cvals['modules'].split(',')]
todos = sorted(chain.from_iterable(imap(getTodos, mods)), key=itemgetter('deadline_cmp'))
tstr = '\n'.join(imap(serializeTodo, todos))
thash = sha1(tstr.encode('utf-8')).hexdigest()

if cvals['thash'] != thash or not os.path.exists(cvals['output']):
	from django.template import Template, Context
	from django.conf import settings

	settings.configure()
	with open(cvals['template'], 'r') as f:
		tpl = Template(f.read())

	html = tpl.render(Context({'todos': todos}))
	with open(cvals['output'], 'w') as f:
		f.write(html.encode('utf-8'))
	Config().setValue('core/thash', thash)
