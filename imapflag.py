#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# imapflag.py - extracts flagged e-mails using IMAP(S)
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
from imaplib import IMAP4, IMAP4_SSL
from datetime import datetime
from itertools import ifilter
from email.utils import mktime_tz, parsedate_tz
from email.header import decode_header

CFGS = ['server', 'user', 'passwd']

class Imapflag:
	def __init__(self):
		cfg = Config()
		for key in CFGS:
			setattr(self, key, str(cfg.value('imapflag/' + key).toString()))
		self.ssl = cfg.value('imapflag/ssl').toBool()

	def getTodos(self):
		self.connectImap()
		try:
			self.imap.login(self.user, self.passwd)
			try:
				self.imap.select()
				_, msgs = self.imap.search(None, 'KEYWORD', '$TODO')
				return map(self.processMessage, msgs[0].split())
			finally:
				self.imap.logout()
		finally:
			try:
				self.imap.shutdown()
			except:
				pass

	def connectImap(self):
		imapclass = IMAP4_SSL if self.ssl else IMAP4
		self.imap = imapclass(self.server)

	def processMessage(self, msg_id):
		_, data = self.imap.fetch(msg_id, '(BODY[HEADER.FIELDS (DATE FROM SUBJECT)])')
		datestr, fromstr, subjectstr = sorted(ifilter(None,
			data[0][1].replace('\r', '').replace('\n ', ' ').split('\n')))
		date = datetime.fromtimestamp(mktime_tz(parsedate_tz(datestr[6:])))
		subject = unicode_header(subjectstr)
		fromaddr = unicode_header(fromstr)
		return {'title': subject, 'deadline': date, 'subtitle': fromaddr}


def unicode_header(encoded):
	return u' '.join(content.decode(charset) if charset else content
		for content, charset in decode_header((encoded.split(' ', 1)[1])))
