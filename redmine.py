#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# redmine.py - extracts open tickets from Redmine (REST WS)
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

from config import Config
from lxml import etree
import requests
import urlparse
from datetime import datetime
import cPickle
import base64
import socket

def getCache():
	return cPickle.loads(base64.b64decode(str(
		Config().value('redmine/cache').toString())))

class NotModified(RuntimeError):
	pass

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
		if urlparse.urlparse(self.url).scheme == '':
			raise Exception('Redmine URL is invalid or empty')
		self.urlbase = self.url.split('.xml', 1)[0] + '/'

	def issue2entry(self, issue):
		dd = issue.xpath('due_date/text()')
		if not dd:
			dl = None
		else:
			dl = datetime.strptime(dd[0], '%Y-%m-%d').date()
		return {
			'subtitle': issue.xpath('project/@name')[0],
			'title': issue.xpath('subject/text()')[0],
			'link': self.urlbase + issue.xpath('id/text()')[0],
			'deadline': dl,
		}

	def getDOM(self):
		cfg = Config()
		etag = str(cfg.value('redmine/etag').toString())
		issues = requests.get(self.url, headers={'If-None-Match': etag})
		try:
			cfg.setValue('redmine/etag', issues.headers['etag'])
		except:
			cfg.remove('redmine/etag')
		if issues.status_code == 304:
			raise NotModified()
		return etree.fromstring(issues.content)

	def getTodos(self):
		try:
			todos = map(self.issue2entry, self.getDOM().xpath('/issues/issue'))
			Config().setValue('redmine/cache',
					base64.b64encode(cPickle.dumps(todos, -1)))
		except (NotModified, requests.exceptions.ConnectionError, socket.error):
			todos = getCache()
		return todos
