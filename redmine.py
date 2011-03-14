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
from xml.dom.minidom import parseString
import urllib2
import urlparse
import datetime

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
		if urlparse.urlparse(self.url).scheme == '':
			raise Exception('Redmine URL is invalid or empty')
		self.urlbase = self.url[:self.url.index('.xml')] + '/';

	def issue2entry(self, issue):
		dd = issue.getElementsByTagName('due_date')[0]
		if len(dd.childNodes) == 0:
			dl = None
		else:
			dl = datetime.datetime.strptime(dd.firstChild.data, '%Y-%m-%d').date()
		return {
			'subtitle': issue.getElementsByTagName('project')[0].attributes['name'].value,
			'title': issue.getElementsByTagName('subject')[0].firstChild.data,
			'link': self.urlbase + issue.getElementsByTagName('id')[0].firstChild.data,
			'deadline': dl,
		}

	def getDOM(self):
		return parseString(urllib2.urlopen(self.url).read())

	def getTodos(self):
		return map(self.issue2entry,
			self.getDOM().documentElement.getElementsByTagName('issue'))
