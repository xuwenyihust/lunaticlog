import pytest
from .. import apache
import asyncio
from asyncio import coroutine
import os



# Testing Class
#class test_apache(object):

def test_heartbeat_lines():
	gen = apache(out_path='./tests/log/test_heartbeat_lines.txt', lines=['heartbeat'], forever=False, count=1)
	gen.run()
	
	try:
		f = open('./tests/log/test_heartbeat_lines.txt')
		line = f.readlines()[0]
		fields = line.split()
		assert len(fields) == 8
	except:
		assert False	
	
	







