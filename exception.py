#!/usr/bin/python3
# -*- coding: utf-8 -*-

class EmptyEnter(Exception):
	"""It the enter is empty or =empty."""
	def __init__(self, message):
		super(EmptyEnter, self).__init__()
		self.message = message

class EnterNotInRange(Exception):
	"""If the enter is not in range."""
	def __init__(self, message):
		super(EnterNotInRange, self).__init__()
		self.message =  message

class EnterNotDigit(Exception):
	"""If the enter is not digit."""
	def __init__(self, message):
		super(EnterNotDigit, self).__init__()
		self.message =  message