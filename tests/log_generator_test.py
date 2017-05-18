import pytest
from .. import apache
import asyncio
from asyncio import coroutine
import os
import re


def test_get_time_field():
	gen = apache()
	try:
		time_field = gen.get_time_field().split()
		time_field0 = time_field[0]
		time_field1 = time_field[1]
		assert time_field1 == '-0700'
		assert len(time_field0.split('/')) == 3
	except:
		assert False


def test_get_ip():
	gen = apache()
	try:
		ip = gen.get_ip()
		assert len(ip.split('.')) == 4
		for x in ip.split('.'):
			assert int(x) in range(0, 256)
	except:
		assert False


def test_get_user_identifier():
	gen = apache()
	try:
		user_identifier = gen.get_user_identifier()
		assert user_identifier == '-'
	except:
		assert False


def test_get_user_id():
	gen = apache()
	try:
		user_id = gen.get_user_id()
		assert user_id == 'frank'
	except:
		assert False


def test_get_method():
	gen = apache()
	try:
		method = gen.get_method()
		assert method in ['GET', 'POST', 'PUT', 'DELETE']
	except:
		assert False


def test_get_resource():
	gen = apache()
	try:
		resource = gen.get_resource()
		assert resource == '/apache_pb.gif'
	except:
		assert False


def test_get_version():
	gen = apache()
	try:
		version = gen.get_version()
		assert version == 'HTTP/1.0'
	except:
		assert False


def test_get_msg():
	gen = apache()
	try:
		msg = gen.get_msg('a', 'b', 'c')
		assert msg == 'a b c'
	except:
		assert False


def test_get_code():
	gen = apache()
	try:
		code = gen.get_code()
		assert code == '200'
	except:
		assert False


def test_get_size():
	gen = apache()
	try:
		size = gen.get_size()
		assert size in range(1024, 10241)
	except:
		assert False


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


# Test param: lines
def test_lines_control():
	gen = apache(out_path='./test_lines_control.txt', lines=['heartbeat', 'access'], methods=['GET', 'PUT', 'POST', 'DELETE'], forever=False, count=10)
	gen.run()

	lines_li = set()

	try:
		f = open('./test_lines_control.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			if log_msg == 'HEARTBEAT':
				lines_li.add('heartbeat')
			else:
				log_method = log_msg.split()[0]
				if log_method in ['GET', 'PUT', 'POST', 'DELETE']:
					lines_li.add('access')

		assert lines_li == set(['heartbeat', 'access'])

	except:
		assert False


# Test param: methods
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

# Test param: methods_p
def test_access_lines_method_dist():
	gen = apache(out_path='./test_access_lines_method_dist.txt', lines=['access'], methods=['GET', 'POST', 'PUT', 'DELETE'], methods_p=[1.0, 0, 0, 0], forever=False, count=3)
	gen.run()

	try:
		f = open('./test_access_lines_method_dist.txt')
		lines = f.readlines()
		for line in lines:
			# Extract the message field
			log_msg = re.findall(r'\"(.*?)\"', line)[0]
			# Extract the http method
			log_method = log_msg.split()[0]
			assert log_method == 'GET'
	except:
		assert False




