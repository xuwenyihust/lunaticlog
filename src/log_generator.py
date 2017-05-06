import os
import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine
import numpy

class log_generator(object):
	
	def __init__(self, log):

		self.a = 0


class access_log_generator(log_generator):

	def __init__(self, log):
		self.log = log

	def run(self):
		self.loop = asyncio.get_event_loop()
		try:
			self.loop.run_until_complete(
				asyncio.wait([
					self.heartbeat_lines()]
					#self.heartbeat_lines(),
					#self.access_lines()]
				)
			)
		finally:
			self.loop.close()


	@coroutine
	def heartbeat_lines(self):
		while True:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			self.log.info('- - - [%s] "%s" - -', t, 'HEARTBEAT')
			yield from asyncio.sleep(1)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", help="log output path")
	parser.add_argument("-m", help="log mode")
	args = parser.parse_args()

	# Identify the log format
	mode = args.m
	# Set default log format
	if not mode:
		mode = 'access'
	# Check if the log format is valid
	if mode not in ['access']:
		print('Argument error: -o')

	# Identufy the output path
	out_path = args.o
	# Set default output path
	if not out_path:
		out_path = './log/lunatic_log.log'

	# Instantiate the logger
	log = logging.getLogger('Gen')
	# Set the level
	logging.basicConfig(level=logging.INFO)
	# Instantiate a file Handler
	out = logging.FileHandler(out_path)

	# Instantiate a Formatter
	# Format the time string
	if mode == 'access':
		log_format = logging.Formatter("%(message)s")
	else:
		log_format = logging.Formatter("%(message)s")

	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	# Load the configure json file to a dict
	#with open(os.environ['LUNATICHOME']+"/config/fake_log_gen.json") as config_file:
	#	config = json.load(config_file)
	

	# Instantiate a log generator
	if mode == 'access':
		log_gen = access_log_generator(log)

	log_gen.run()


if __name__ == "__main__":
	main()

