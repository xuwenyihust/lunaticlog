import os
import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine
import numpy
from subprocess import check_call
import abc

#################################
##
##  Abstract Base Log Generator
##
#################################
class log_gen(metaclass=abc.ABCMeta):

	@abc.abstractproperty
	def lines(self):
		pass

	@abc.abstractproperty
	def methods(self):
		pass

	@abc.abstractproperty
	def methods_p(self):
		pass

	@abc.abstractproperty
	def mode(self):
		pass

	@abc.abstractproperty
	def out_format(self):
		pass

	@abc.abstractmethod
	def run(self):
		pass
		

#################################
##
## Apache Access Log Generator
##
#################################
class apache_gen(log_gen):

	def __init__(self, out_path='./apache.log', out_format=['stdout', 'log'], lines=['heartbeat', 'access'], heartbeat_interval=0.1, access_interval=[0.1, 2], methods=['GET', 'POST', 'PUT', 'DELETE'], methods_p = [0.7, 0.1, 0.1, 0.1], mode='uniform', forever=True, count=1):
		# Assign the lines to generate	
		self._lines_full = ['heartbeat', 'access']
		self._lines_gen = [self.heartbeat_lines(), self.access_lines()]
		self._lines = lines
		# Assign the http methods to generate	
		self._methods = methods
		# Assign the methods distribution
		self._methods_p = methods_p
		# Run forever or not
		self._forever = forever
		# Total # of logs to generate
		self._count = count
		# Assign the intervals
		self._heartbeat_interval = heartbeat_interval
		self._access_interval = access_interval
		# Assign the generator mode
		self._mode = mode

		# Assign the output format
		self._out_format = out_format
		# Assign the output path
		self._out_log = out_path
		if 'log' in self.out_format or 'gzip' in self.out_format:
			self.f_log = open(self.out_log, 'w')
		#self.out_gz

	# Predefined lines_full
	# ['heartbeat', 'access']
	@property
	def lines_full(self):
		return self._lines_full

	# Predefined lines_gen
	# [self.heartbeat_lines(), self.access_lines()] 
	@property
	def lines_gen(self):
		return self._lines_gen

	@property
	def lines(self):
		return self._lines

	@lines.setter
	def lines(self, val):
		if type(val) != type([1,2,3]):
			raise Exception('lines should be a list.')
		lines_set = set(val)
		lines_full_set = set(self.lines_full)
		if not lines_set.issubset(lines_full_set):
			raise Exception("Unsupported line types.")
		if len(lines_set) != len(val):
			raise Exception("Duplicated line types.")
		self._lines = val

	@property
	def methods(self):
		return self._methods

	@methods.setter
	def methods(self, val):
		if type(val) != type([1,2,3]):
			raise Exception('methods should be a list.')
		methods_set = set(val)
		methods_full_set = set(['GET', 'POST', 'PUT', 'DELETE'])
		if not methods_set.issubset(methods_full_set):
			raise Exception("Unsupported method types.")
		if len(methods_set) != len(val):
			raise Exception("Duplicated method types.")
		self._methods = val

	@property
	def methods_p(self):
		return self._methods_p

	@methods_p.setter
	def methods_p(self, val):
		if type(val) != type([1,2,3]):
			raise Exception('methods_p should be a list.')
		if len(val) != len(self.methods):
			raise Exception("Length of methods_p doesn't equal length of methods.")
		if abs(1-sum(val)) > 0.01:
			raise Exception("Sum of methods_p must equals 1.")
		for x in val:
			if x < 0 or x > 1:
				raise Exception("All members of methods_p must be in the range of 0 to 1 ")	
		self._methods_p = val

	@property
	def forever(self):
		return self._forever

	@forever.setter
	def forever(self, val):
		if val not in [True, False]:
			raise Exception("forever must be either True or False")
		self._forever = val

	@property
	def count(self):
		return self._count
		
	@count.setter
	def count(self, val):
		self._count = val

	@property
	def heartbeat_interval(self):
		return self._heartbeat_interval

	# When given heartbeat_interval, 
	# heartbeat must be one of the methods to be generated
	@heartbeat_interval.setter
	def heartbeat_interval(self, val):
		if type(val) != type(1) and type(val) != type(0.5):
			raise Exception("heartbeat_interval value should be either integer or decimal")
		if val is not None and 'heartbeat' not in self.lines:
			raise Exception("Only set heartbeat_interval when generate heartbeat")
		self._heartbeat_interval = val

	@property
	def access_interval(self):
		return self._access_interval

	@access_interval.setter
	def access_interval(self, val):
		if type(val) != type([1,2,3]):
			raise Exception("access_interval should be a list")
		if len(val) != 2:
			raise Exception("access_interval should be a list containing 2 elements")
		if type(val[0]) != type(1) and type(val[0]) != type(0.5):
			raise Exception("access_interval[0] should be either integer or decimal")
		if type(val[1]) != type(1) and type(val[1]) != type(0.5):
			raise Exception("access_interval[1] should be either integer or decimal")
		if val[0] >= val[1]:
			raise Exception("access_interval[0] should be smaller than access_interval[1]")
		self._access_interval = val

	@property
	def mode(self):
		return self._mode

	@mode.setter
	def mode(self, val):
		if val not in ['uniform', 'push', 'spike']:
			raise Exception("Unrecognized mode")

	@property
	def out_format(self):
		return self._out_format

	@out_format.setter
	def out_format(self, val):
		if type(val) != type([1,2,3]):
			raise Exception("out_format should be a list")
		if len(val) == 0:
			raise Exception("Should select at least 1 output format")
		out_format_set = set(val)
		if not out_format_set.issubset(set(['stdout', 'log', 'gzip'])):
			raise Exception("Unsupported output format")
		self._out_format = val

	@property
	def out_log(self):
		return self._out_log


	def run(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		try:
			loop.run_until_complete(
				asyncio.wait([self.lines_gen[self.lines_full.index(x)] for x in self.lines])
		)
		finally:
			loop.close()
			if 'log' in self.out_format or 'gzip' in self.out_format:
				self.f_log.close()
				if 'gzip' in self.out_format:
					check_call(['gzip', self.out_log])



	@coroutine
	def heartbeat_lines(self):
		while self.forever or self.count > 0:
			t = self.get_time_field()
			self.output_heartbeat(t)
			#self.log.info('- - - [%s] "%s" - -', t, 'HEARTBEAT')	
			if self.count > 0:
				self.count -= 1
			yield from asyncio.sleep(self.heartbeat_interval)

	# Output the heartbeat line (to stdout, file, ...)
	def output_heartbeat(self, t):
		string = '- - - [' + t + '] "' + 'HEARTBEAT" - -'
		if 'stdout' in self.out_format:
			print(string)
		if 'log' in self.out_format:
			self.f_log.write(string + '\n')

	# Derive the timestamp from current time
	def get_time_field(self):
		return datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')


	@coroutine
	def access_lines(self):
		while self.forever or self.count > 0:	
			# Generate different fields in the access log
			ip = self.get_ip()
			user_identifier = self.get_user_identifier()
			user_id = self.get_user_id()
			t = self.get_time_field()
			method = self.get_method()
			resource = self.get_resource()
			version = self.get_version()
			msg = self.get_msg(method, resource, version)
		
			code = self.get_code()
			size = self.get_size()
			# Output the generated access line	
			self.output_access(ip, user_identifier, user_id, t, msg, code, size)
			# Decrease the counter
			if self.count > 0:
				self.count -= 1


			sleep_time = self.get_access_sleep_time()
			yield from asyncio.sleep(sleep_time)


	
	# Output the access line (to stdout, file, ...)
	def output_access(self, ip, user_identifier, user_id, t, msg, code, size):
		string = ip+' '+user_identifier+' '+user_id+' '+'['+t+'] "'+msg+'" '+code+' '+str(size)
		if 'stdout' in self.out_format:
			print(string)
		if 'log' in self.out_format:
			self.f_log.write(string + '\n')


	# Generate the ip field for the access line
	def get_ip(self):
		return '.'.join(str(random.randint(0, 255)) for i in range(4))

	# Generate the user_identifier field for the access line
	def get_user_identifier(self):
		return '-'

	# Generate the user_id field for the access line
	def get_user_id(self):
		return 'frank'

	# Generate the HTTP method field for the access line
	def get_method(self):
		return numpy.random.choice(self.methods, p=self.methods_p)

	# Generate the resource field for the access line
	def get_resource(self):
		return '/apache_pb.gif'
	
	# Generate the version field for the access line
	def get_version(self):
		return 'HTTP/1.0'

	# Generate the message field for the access line
	def get_msg(self, method, resource, version):
		return method + " " + resource + " " + version

	# Generate the HTTP code field for the access line
	def get_code(self):
		return '200'

	# Generate the message size field for the access line
	def get_size(self):
		return random.randint(1024, 10240)


	def get_access_sleep_time(self):
		# 'normal' mode - uniform distribution between min & max intervals
		if self.mode == 'uniform':
			return random.uniform(self.access_interval[0], self.access_interval[1])
		# 'push' mode - at highest rate
		elif self.mode == 'push':
			return self.access_interval[0]

		# 'spike' mode
		elif self.mode == 'spike':
			mean = (self.access_interval[0]+self.access_interval[1])/2
			# Standard deviation
			sigma = (self.access_interval[1]-self.access_interval[0])/2
			return numpy.random.normal(mean, sigma)

		else:
			random.uniform(self.access_interval[0], self.access_interval[1])




