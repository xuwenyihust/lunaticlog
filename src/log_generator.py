import os
import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine
import numpy


# Apache Access Logs
class apache(object):

	def __init__(self, out_path='./apache.log', lines=['heartbeat', 'access'], methods=['GET', 'POST', 'PUT', 'DELETE'], forever=True, count=1):
		# Assign the lines to generate
		self.lines = lines
		self.lines_full = ['heartbeat', 'access']
		self.lines_gen = [self.heartbeat_lines(), self.access_lines()]
		# Assign the http methods to generate
		self.methods = methods	
		# Run forever or not
		self.forever = forever
		# Total # of logs to generate
		self.count = count

		# Instantiate the logger
		self.log = logging.getLogger('Gen')
		# Set the level
		logging.basicConfig(level=logging.INFO)
		# Instantiate a file Handler
		out = logging.FileHandler(out_path, mode='w')

		log_format = logging.Formatter("%(message)s")
		# Set the Formatter for this Handler to form
		out.setFormatter(log_format)
		# Add the file Handler 'out' to the logger'log'
		self.log.addHandler(out)

		#self.loop = asyncio.get_event_loop()

	def run(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		try:
			loop.run_until_complete(
				asyncio.wait([self.lines_gen[self.lines_full.index(x)] for x in self.lines])
		)
		finally:
			loop.close()



	@coroutine
	def heartbeat_lines(self):
		while self.forever or self.count > 0:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			self.log.info('- - - [%s] "%s" - -', t, 'HEARTBEAT')
			if self.count > 0:
				self.count -= 1
			yield from asyncio.sleep(1)


	@coroutine
	def access_lines(self):
		while self.forever or self.count > 0:
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			user_identifier = '-'
			user_id = 'frank'
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')

			#method = numpy.random.choice(self.methods, p=self.methods_dist)
			method = random.choice(self.methods)
			#resource = self.resources[random.randint(0, len(self.resources)-1)]
			resource = '/apache_pb.gif'
			#version = self.versions[random.randint(0, len(self.versions)-1)]
			version = 'HTTP/1.0'
			msg = method + " " + resource + " " + version
			#code = numpy.random.choice(self.codes, p=self.codes_dist)
			code = '200'
			size = random.randint(1024, 10240)
			self.log.info('%s %s %s [%s] "%s" %s %s', ip, user_identifier, user_id, t, msg, code, size)
			if self.count > 0:
				self.count -= 1
			yield from asyncio.sleep(random.randint(1, 5))





