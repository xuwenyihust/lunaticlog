[![Python](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)](https://travis-ci.org/xuwenyihust/Visor)
[![PyPI version](https://badge.fury.io/py/lunaticlog.svg)](https://badge.fury.io/py/lunaticlog)
[![Travis](https://travis-ci.org/xuwenyihust/lunaticlog.svg?branch=master)](https://travis-ci.org/xuwenyihust/lunaticlog)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/xuwenyihust/lunaticlog.svg)](http://isitmaintained.com/project/xuwenyihust/lunaticlog "Percentage of issues still open")
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/xuwenyihust/Visor/blob/master/LICENSE)


# Lunaticlog
Log loads generator, test if your system can survive under the log spikes.


## Supported Log Format
What kinds of log formats does it support now?

* Apache Access Log

`127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326`


## Install

`pip install lunaticlog`


## Parameters

* `-m` The log generator mode, which log format to generate.

* `-o` The output log file path.


## License
See the LICENSE file for license rights and limitations (MIT).

