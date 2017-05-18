[![Python](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)](https://travis-ci.org/xuwenyihust/Visor)
[![PyPI version](https://badge.fury.io/py/lunaticlog.svg)](https://badge.fury.io/py/lunaticlog)
[![Travis](https://travis-ci.org/xuwenyihust/lunaticlog.svg?branch=master)](https://travis-ci.org/xuwenyihust/lunaticlog)
[![Coverage Status](https://coveralls.io/repos/github/xuwenyihust/lunaticlog/badge.svg?branch=master)](https://coveralls.io/github/xuwenyihust/lunaticlog?branch=master)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/xuwenyihust/lunaticlog.svg)](http://isitmaintained.com/project/xuwenyihust/lunaticlog "Percentage of issues still open")
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/xuwenyihust/Visor/blob/master/LICENSE)


# Lunaticlog
Lunaticlog is a mock HTTP log generator package, use it's fake log workloads to test if your monitor / analyzer can survive various extreme conditions. 


## Documentation
Lunaticlog's documentation can be found on https://xuwenyihust.github.io/lunaticlog/lunaticlog/html/.


## Overview
Lunaticlog can generate logs with customized contents. The log traffic can also be configured.

### Supported Log Format
What kinds of log formats does it support now?

* Apache Access Log

  `127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326`

* [TODO] Nginx Access Log

* [TODO] Amazon S3 Log

### Log Generation Mode
The fate of lunaticlog is to create chaos to test your system. So it needs to generate various extreme cases, such as sudden traffic spikes.

What traffic modes are supported now?

* **uniform** 

  Generate logs at a random rate, which is uniformly distributed.

* **push**

  Generate logs at highest speed(whihch can be configured).

* **spike**

  Generate logs at sudden very high rates periodically.
  
<img src="https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_uniform.png" width="320" height="240"/><img src="https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_spike.png" width="320" height="240"/><img src="https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_push.png" width="320" height="240"/>

The scripts to plot these bandwidth charts can be found under `./scripts`.

### Output Formats

* STDOUT

* `.log` file

* `.gz` file


## Install

`pip install lunaticlog`


## Usage Example

### apache Class

```python
from lunaticlog import apache

log_gen = apache(out_path='./apache.log', lines=['heartbeat', 'access'])
log_gen.run()
```

## License
See the LICENSE file for license rights and limitations (MIT).

