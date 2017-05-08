from setuptools import setup, find_packages

# Parse the requirements.txt to get the dependencies
#with open('requirements.txt') as f:
#	required = f.read().splitlines()

setup(
	name = 'lunaticlog',
	version = '0.1.0',
	description = 'A log generator to test your monitor system.',
	url = 'https://github.com/xuwenyihust/lunaticlog',
	author = 'Wenyi Xu',
	author_email = 'wenyixu101@gmail.com',
	license = 'MIT',
	keywords='log monitor apache',

	packages = find_packages(),

#	install_requires = required,

	package_data={
   		'configuration': ['conf/*.json'],
	},

	test_suite = 'tests',
	setup_requires=['pytest-runner'],
	tests_require = ['pytest']
)
