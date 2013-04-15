#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# github_issues.py - extracts issues of your GitHub repos
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
from datetime import datetime
import json, re, requests

CFGS = ['user', 'passwd']

class Github_issues:
	def __init__(self):
		cfg = Config()
		self.session = requests.Session()
		self.session.auth = tuple(
			str(cfg.value('github_issues/' + key).toString()) for key in CFGS)

	def getTodos(self):
		issues = self.session.get('https://api.github.com/issues')
		return map(issue2entry, json.loads(issues.content))


HTML_RE = re.compile('github.com/[^/]+/([^/]+)/issues')
def issue2entry(issue):
	url = issue['html_url']
	try:
		due = issue['milestone']['due_on']
	except (KeyError, TypeError):
		due = issue['created_at']
	return {
			'subtitle': HTML_RE.search(url).group(1),
			'title': issue['title'],
			'link': url,
			'deadline': datetime.strptime(due, '%Y-%m-%dT%H:%M:%SZ'),
			}
