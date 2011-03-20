#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# orgmode.py - extracts TODOs from Org-mode files
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

import Orgnode
import os
from config import Config

class Orgmode:
	def __init__(self):
		self.dir = unicode(Config().value('orgmode/dir').toString())
		if not os.path.isdir(self.dir):
			raise Exception('Org-mode directory is invalid or empty')

	def subtitle(self, parents):
		return '/'.join(map(Orgnode.Orgnode.Heading, parents))

	def getTodos(self):
		ls = filter(lambda x: x.endswith('.org'), os.listdir(self.dir))
		result = list()
		for f in ls:
			fn = os.path.join(self.dir, f)
			nodes = Orgnode.makelist(fn)
			parents = list()
			for node in nodes:
				lvl = node.Level()
				while len(parents) >= lvl:
					parents.pop()
				if node.Todo() == 'TODO':
					result.append({'title': node.Heading(), 'deadline': node.Deadline(),
						'scheduled': node.Scheduled(),
						'link': 'file://' + fn, 'subtitle': self.subtitle(parents)})
				parents.append(node)
		return result
