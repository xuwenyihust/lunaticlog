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


# Apache Access Logs
class apache_gen(object):

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
		return val

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
		return val

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
		return val

	@property
	def forever(self):
		return self._forever

	@forever.setter
	def forever(self, val):
		if val not in [True, False]:
			raise Exception("forever must be either True or False")
		return val

	@property
	def count(self):
		return self._count

	@property
	def heartbeat_interval(self):
		return self._heartbeat_interval

	# When given heartbeat_interval, 
	# heartbeat must be one of the methods to be generated
	@heartbeat_interval.setter
	def heartbeat_interval(self, val):
		if val is not None and 'heartbeat' not in self.lines:
			raise Exception('an only set heartbeat_interval when generate heartbeat')
		return val

	@property
	def access_interval(self):
		return self._access_interval

	@property
	def mode(self):
		return self._mode

	@property
	def out_format(self):
		return self._out_format

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

	def output_heartbeat(self, t):
		string = '- - - [' + t + '] "' + 'HEARTBEAT" - -'
		if 'stdout' in self.out_format:
			print(string)
		if 'log' in self.out_format:
			self.f_log.write(string + '\n')

	def get_time_field(self):
		return datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')


	@coroutine
	def access_lines(self):
		while self.forever or self.count > 0:	
			ip = self.get_ip()
			user_identifier = self.get_user_identifier()
			user_id = self.get_user_id()
			t = self.get_time_field()

			method = self.get_method()
			#method = random.choice(self.methods)
			#resource = self.resources[random.randint(0, len(self.resources)-1)]
			resource = self.get_resource()
			#version = self.versions[random.randint(0, len(self.versions)-1)]
			version = self.get_version()
			msg = self.get_msg(method, resource, version)
			#code = numpy.random.choice(self.codes, p=self.codes_dist)
			#code = '200'
			code = self.get_code()
			#size = random.randint(1024, 10240)
			size = self.get_size()
			#self.log.info('%s %s %s [%s] "%s" %s %s', ip, user_identifier, user_id, t, msg, code, size)
			self.output_access(ip, user_identifier, user_id, t, msg, code, size)

			if self.count > 0:
				self.count -= 1


			sleep_time = self.get_access_sleep_time()
			yield from asyncio.sleep(sleep_time)


	#def assign_lines(self, lines):
	#	lines_set = set(lines)
	#	lines_full_set = set(self.lines_full)

	#	if not lines_set.issubset(lines_full_set):
	#		raise Exception("Unsupported line types.")
	#	if len(lines_set) != len(lines):
	#		raise Exception("Duplicated line types.")
	#	return lines


	#def assign_methods(self, methods):
	#	methods_set = set(methods)
	#	methods_full_set = set(['GET', 'POST', 'PUT', 'DELETE'])

	#	if not methods_set.issubset(methods_full_set):
	#		raise Exception("Unsupported method types.")
	#	if len(methods_set) != len(methods):
	#		raise Exception("Duplicated method types.")
	#	return methods


	#def assign_methods_p(self, methods_p):
	#	if len(methods_p) != len(self._methods):
	#		raise Exception("Length of methods_p doesn't equal length of methods.")
	#	if abs(1-sum(methods_p)) > 0.01:
	#		raise Exception("Sum of methods_p must equals 1.")
	#	for x in methods_p:
	#		if x < 0 or x > 1:
	#			raise Exception("All members of methods_p must be in the range of 0 to 1 ")	
	#	return methods_p
	

	def output_access(self, ip, user_identifier, user_id, t, msg, code, size):
		string = ip+' '+user_identifier+' '+user_id+' '+'['+t+'] "'+msg+'" '+code+' '+str(size)
		if 'stdout' in self.out_format:
			print(string)
		if 'log' in self.out_format:
			self.f_log.write(string + '\n')



	def get_ip(self):
		return '.'.join(str(random.randint(0, 255)) for i in range(4))


	def get_user_identifier(self):
		return '-'


	def get_user_id(self):
		return 'frank'


	def get_method(self):
		return numpy.random.choice(self.methods, p=self.methods_p)


	def get_resource(self):
		return '/apache_pb.gif'
	

	def get_version(self):
		return 'HTTP/1.0'


	def get_msg(self, method, resource, version):
		return method + " " + resource + " " + version


	def get_code(self):
		return '200'


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




