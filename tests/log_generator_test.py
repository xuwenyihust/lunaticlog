import pytest
from .. import apache
import asyncio
from asyncio import coroutine
import os
import re


def test_heartbeat_lines_format():
	gen = apache(out_path='./test_heartbeat_lines_format.txt', lines=['heartbeat'], forever=False, count=1)
	gen.run()
	
	try:
		f = open('./test_heartbeat_lines_format.txt')
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
	gen = apache(out_path='./test_access_lines_format.txt', lines=['access'], forever=False, count=1)
	gen.run()

	try:
		f = open('./test_access_lines_format.txt')
		line = f.readlines()[0]
		# Extract the time field
		log_time = re.findall(r'\[(.*?)\]', line)
		assert len(log_time) == 1
		# Extract the message field
		log_msg = re.findall(r'\"(.*?)\"', line)
		assert len(log_msg) == 1

	except:
		assert False


def test_access_lines_method():
	# Test GET generation
	gen = apache(out_path='./test_access_lines_method.txt', lines=['access'], methods=['GET'], forever=False, count=3)
	gen.run()

	try:
		f = open('./test_access_lines_method.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			# Extract the http method
			log_method = log_msg.split()[0]
			assert log_method == 'GET'

	except:
		assert False

	# Test PUT generation
	gen = apache(out_path='./test_access_lines_method.txt', lines=['access'], methods=['PUT'], forever=False, count=3)
	gen.run()

	try:
		f = open('./test_access_lines_method.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			# Extract the http method
			log_method = log_msg.split()[0]
			assert log_method == 'PUT'

	except:
		assert False

	# Test POST generation
	gen = apache(out_path='./test_access_lines_method.txt', lines=['access'], methods=['POST'], forever=False, count=3)
	gen.run()

	try:
		f = open('./test_access_lines_method.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			# Extract the http method
			log_method = log_msg.split()[0]
			assert log_method == 'POST'
	except:
		assert False

	# Test DELETE generation
	gen = apache(out_path='./test_access_lines_method.txt', lines=['access'], methods=['DELETE'], forever=False, count=3)
	gen.run()

	try:
		f = open('./test_access_lines_method.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			# Extract the http method
			log_method = log_msg.split()[0]
			assert log_method == 'DELETE'
	except:
		assert False







