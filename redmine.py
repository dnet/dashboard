#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# redmine.py - extracts open tickets from Redmine (Atom feed)
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
import feedparser
import urlparse
import re

class Redmine:
	def __init__(self):
		self.url = unicode(Config().value('redmine/url').toString())
		if urlparse.urlparse(self.url).scheme == '':
			raise Exception('Redmine URL is invalid or empty')
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
