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
import urllib2
import urlparse
from datetime import datetime
import cPickle
from StringIO import StringIO
import base64

def getCache():
	return cPickle.loads(base64.b64decode(str(
		Config().value('redmine/cache').toString())))

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
		if urlparse.urlparse(self.url).scheme == '':
			raise Exception('Redmine URL is invalid or empty')
		self.urlbase = self.url[:self.url.index('.xml')] + '/'

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
		req = urllib2.Request(self.url)
		req.add_header('If-None-Match', str(cfg.value('redmine/etag').toString()))
		issues = urllib2.urlopen(req)
		try:
			cfg.setValue('redmine/etag', issues.info()['ETag'])
		except:
			cfg.remove('redmine/etag')
		return etree.fromstring(issues.read())

	def getTodos(self):
		try:
			todos = map(self.issue2entry, self.getDOM().xpath('/issues/issue'))
			output = StringIO()
			cPickle.dump(todos, output, -1)
			Config().setValue('redmine/cache', base64.b64encode(output.getvalue()))
		except urllib2.HTTPError as e:
			if e.code != 304:
				raise
			todos = getCache()
		except urllib2.URLError as e:
			todos = getCache()
		return todos
