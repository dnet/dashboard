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
