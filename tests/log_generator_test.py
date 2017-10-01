import pytest
from .. import log_gen
from .. import apache_gen
import asyncio
from asyncio import coroutine
import os
import re
import json

##########################################
#####
#####	Test Abstract Class
#####
##########################################
def test_abstract_class():

	try:
		gen = log_gen()
		assert False, 'Abstract class instance created!'
	except TypeError:
		pass

	try:
		class one_log_gen(log_gen):
			@property
			def methods(self):
				pass
			@property
			def methods_p(self):
				pass
			@property
			def mode(self):
				pass
			@property
			def out_format(self):
				pass
			def run(self):
				pass
		gen = one_log_gen()
		assert False, "Abstract class property not implemented" 
	except TypeError:
		pass

	try:
		class one_log_gen(log_gen):
			@property
			def lines(self):
				pass
			@property
			def method(self):
				pass
			@property
			def methods_p(self):
				pass
			@property
			def mode(self):
				pass
			@property
			def out_format(self):
				pass
		gen = one_log_gen()
		assert False, "Abstract class method not implemented"
	except TypeError:
		pass

##########################################
#####
#####	Test Apache Attribute Setting
#####
##########################################

def test_attr_lines():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.lines = set('access')
	assert str(error_info.value) == 'lines should be a list.'

	with pytest.raises(Exception) as error_info:
		gen.lines = ['whatever']
	assert str(error_info.value) == "Unsupported line types."

	with pytest.raises(Exception) as error_info:
		gen.lines = ['access', 'access']
	assert str(error_info.value) == "Duplicated line types."


def test_attr_methods():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.methods = set(['GET', 'POP', 'PUT', 'DELETE'])
	assert str(error_info.value) == 'methods should be a list.'

	with pytest.raises(Exception) as error_info:
		gen.methods = ['GET', 'POP', 'PUT', 'DELETE']
	assert str(error_info.value) == "Unsupported method types."

	with pytest.raises(Exception) as error_info:
		gen.methods = ['GET', 'GET', 'POST', 'PUT', 'DELETE']
	assert str(error_info.value) == "Duplicated method types."


def test_attr_methods_p():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.methods_p = set([0.6, 0.4])	
	assert str(error_info.value) == 'methods_p should be a list.'

	with pytest.raises(Exception) as error_info:
		gen.methods = ['GET', 'POST', 'PUT', 'DELETE']
		gen.methods_p = [0.5, 0.5]
	assert str(error_info.value) == "Length of methods_p doesn't equal length of methods." 

	with pytest.raises(Exception) as error_info:
		gen.methods = ['GET', 'POST', 'PUT', 'DELETE']
		gen.methods_p = [0.6, 0.7, 0.1, 0.1]
	assert str(error_info.value) == "Sum of methods_p must equals 1."

	with pytest.raises(Exception) as error_info:
		gen.methods_p = [-1, 1, 0.5, 0.5]
	assert str(error_info.value) == "All members of methods_p must be in the range of 0 to 1 "


def test_attr_forever():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.forever = 'AHA'
	assert str(error_info.value) == "forever must be either True or False"


def test_attr_heartbeat_interval():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.heartbeat_interval = '0.1'
	assert str(error_info.value) == "heartbeat_interval value should be either integer or decimal"

	with pytest.raises(Exception) as error_info:
		gen.lines = ['access']
		gen.heartbeat_interval = 0.1
	assert str(error_info.value) == "Only set heartbeat_interval when generate heartbeat"
	

def test_attr_access_interval():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.access_interval = 1
	assert str(error_info.value) == "access_interval should be a list"
	
	with pytest.raises(Exception) as error_info:
		gen.access_interval = set([1,2])
	assert str(error_info.value) == "access_interval should be a list"

	with pytest.raises(Exception) as error_info:
		gen.access_interval = [1]
	assert str(error_info.value) == "access_interval should be a list containing 2 elements"

	with pytest.raises(Exception) as error_info:
		gen.access_interval = ['1', 2]
	assert str(error_info.value) == "access_interval[0] should be either integer or decimal"

	with pytest.raises(Exception) as error_info:
		gen.access_interval = [1, '2']
	assert str(error_info.value) == "access_interval[1] should be either integer or decimal"

	with pytest.raises(Exception) as error_info:
		gen.access_interval = [2, 1]
	assert str(error_info.value) == "access_interval[0] should be smaller than access_interval[1]"


def test_attr_mode():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.mode = 'drama'
	assert str(error_info.value) == "Unrecognized mode"


def test_attr_out_format():
	gen = apache_gen()
	with pytest.raises(Exception) as error_info:
		gen.out_format = 'log'
	assert str(error_info.value) == "out_format should be a list"

	with pytest.raises(Exception) as error_info:
		gen.out_format = []
	assert str(error_info.value) == "Should select at least 1 output format"
	
	with pytest.raises(Exception) as error_info:
		gen.out_format = ['stdout', 'cat']
	assert str(error_info.value) == "Unsupported output format"


##########################################
#####
#####   Test 
#####
##########################################


def test_get_time_field():
	gen = apache_gen()
	try:
		time_field = gen.get_time_field().split()
		time_field0 = time_field[0]
		time_field1 = time_field[1]
		assert time_field1 == '-0700'
		assert len(time_field0.split('/')) == 3
	except:
		assert False


def test_get_ip():
	gen = apache_gen()
	try:
		ip = gen.get_ip()
		assert len(ip.split('.')) == 4
		for x in ip.split('.'):
			assert int(x) in range(0, 256)
	except:
		assert False


def test_get_user_identifier():
	gen = apache_gen()
	try:
		user_identifier = gen.get_user_identifier()
		assert user_identifier == '-'
	except:
		assert False


def test_get_user_id():
	gen = apache_gen()
	config_file = './config/apache_gen.json'
	with open(config_file, 'r') as f:
		config = json.load(f)
	try:
		user_id = gen.get_user_id()
		assert user_id in config["user_id"]
	except:
		assert False


def test_get_method():
	gen = apache_gen()
	try:
		method = gen.get_method()
		assert method in ['GET', 'POST', 'PUT', 'DELETE']
	except:
		assert False


def test_get_resource():
	gen = apache_gen()
	try:
		resource = gen.get_resource()
		assert resource == '/apache_pb.gif'
	except:
		assert False


def test_get_version():
	gen = apache_gen()
	try:
		version = gen.get_version()
		assert version == 'HTTP/1.0'
	except:
		assert False


def test_get_msg():
	gen = apache_gen()
	try:
		msg = gen.get_msg('a', 'b', 'c')
		assert msg == 'a b c'
	except:
		assert False


def test_get_code():
	gen = apache_gen()
	try:
		code = gen.get_code()
		assert code == '200'
	except:
		assert False


def test_get_size():
	gen = apache_gen()
	try:
		size = gen.get_size()
		assert size in range(1024, 10241)
	except:
		assert False


def test_heartbeat_lines_format():
	gen = apache_gen(out_path='./test_heartbeat_lines_format.txt', forever=False, count=1)
	gen.lines = ['heartbeat']
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
	gen = apache_gen(out_path='./test_access_lines_format.txt', forever=False, count=1)
	gen.lines = ['access']
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
'''def test_lines_control():
	gen = apache_gen(out_path='./test_lines_control.txt', lines=['heartbeat', 'access'], methods=['GET', 'PUT', 'POST', 'DELETE'], forever=False, count=10)
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
	gen = apache_gen(out_path='./test_access_lines_method.txt', lines=['access'], methods=['GET'], forever=False, count=3)
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
	gen = apache_gen(out_path='./test_access_lines_method.txt', lines=['access'], methods=['PUT'], forever=False, count=3)
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
	gen = apache_gen(out_path='./test_access_lines_method.txt', lines=['access'], methods=['POST'], forever=False, count=3)
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
	gen = apache_genout_path='./test_access_lines_method.txt', lines=['access'], methods=['DELETE'], forever=False, count=3)
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
	gen = apache_gen(out_path='./test_access_lines_method_dist.txt', lines=['access'], methods=['GET', 'POST', 'PUT', 'DELETE'], methods_p=[1.0, 0, 0, 0], forever=False, count=3)
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
'''



