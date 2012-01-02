#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# aleph_loaned.py - scrapes loaned books from Aleph systems
#
# Copyright (c) 2012 András Veres-Szentkirályi
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
from aleph import Aleph

CFGS = ['url', 'username', 'password']

class Aleph_loaned:
	def __init__(self):
		self.url = str(Config().value('aleph_loaned/url').toString())
		self.aleph = Aleph()

	def getTodos(self):
		cfg = Config()
		self.aleph.login(*[str(cfg.value('aleph_loaned/' + key).toString()) for key in CFGS])
		try:
			return map(self.loan2entry, self.aleph.get_loaned())
		finally:
			self.aleph.logout()

	def loan2entry(self, loan):
		return {
				'subtitle': loan['author'],
				'title': loan['title'],
				'link': self.url,
				'deadline': loan['due'],
				}
