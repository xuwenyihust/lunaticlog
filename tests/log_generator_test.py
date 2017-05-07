import pytest
from .. import apache
import asyncio
from asyncio import coroutine
import os
import re


def test_heartbeat_lines_format():
	gen = apache(out_path='./test_heartbeat_lines.txt', lines=['heartbeat'], forever=False, count=1)
	gen.run()
	
	try:
		f = open('./test_heartbeat_lines.txt')
		line = f.readlines()[0]
		#fields = line.split()
		#assert len(fields) == 8
		# Extract the time field
		log_time = re.findall(r'\[(.*?)\]', line)
		assert len(log_time) == 1
		# Extract the message field
		log_msg = re.findall(r'\"(.*?)\"', line)
		assert len(log_msg) == 1
		assert log_msg[0] == 'HEARTBEAT'
	except:
		assert False	

	
def	test_access_lines_format():
	gen = apache(out_path='./test_access_lines.txt', lines=['access'], forever=False, count=1)
	gen.run()

	try:
		f = open('./test_access_lines.txt')
		line = f.readlines()[0]
		# Extract the time field
		log_time = re.findall(r'\[(.*?)\]', line)
		assert len(log_time) == 1
		# Extract the message field
		log_msg = re.findall(r'\"(.*?)\"', line)
		assert len(log_msg) == 1

	except:
		assert False



