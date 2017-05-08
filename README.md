[![Python](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)](https://travis-ci.org/xuwenyihust/Visor)
[![PyPI version](https://badge.fury.io/py/lunaticlog.svg)](https://badge.fury.io/py/lunaticlog)
[![Travis](https://travis-ci.org/xuwenyihust/lunaticlog.svg?branch=master)](https://travis-ci.org/xuwenyihust/lunaticlog)
[![Coverage Status](https://coveralls.io/repos/github/xuwenyihust/lunaticlog/badge.svg?branch=issue-34)](https://coveralls.io/github/xuwenyihust/lunaticlog?branch=issue-34)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/xuwenyihust/lunaticlog.svg)](http://isitmaintained.com/project/xuwenyihust/lunaticlog "Percentage of issues still open")
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/xuwenyihust/Visor/blob/master/LICENSE)


# Lunaticlog
Lunaticlog is a mock HTTP log generator package, use it to test if your monitor can survive under different conditions. 


## Documentation
Lunaticlog's documentation can be found on https://xuwenyihust.github.io//lunaticlog/.


## Overview
Lunaticlog can generate logs with customized contents. The log traffic can also be configured.

## Supported Log Format
What kinds of log formats does it support now?

* Apache Access Log

  `127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326`


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

