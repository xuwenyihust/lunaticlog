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

  `123.65.150.10 - - [23/Aug/2010:03:50:59 +0000] "POST /wordpress3/wp-admin/admin-ajax.php HTTP/1.1" 200 2 "http://www.example.com/wordpress3/wp-admin/post-new.php" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3"`

* [TODO] Amazon S3 Log

  `79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be mybucket [06/Feb/2014:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /mybucket?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" -`

### Log Rotation
Set attribute `rotation_size` to rotate logs when current log file achieves the max size.

### Log Generation Mode
The fate of lunaticlog is to create chaos to test your system. So it needs to generate various extreme cases, such as sudden traffic spikes.

What traffic modes are supported now?

* **uniform** 

  Generate logs at a random rate, which is uniformly distributed.

* **push**

  Generate logs at highest speed(which can be configured).

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

### apache_gen Class

**Instantiation**

```python
from lunaticlog import apache_gen

log_gen = apache_gen(out_path='./apache.log', lines=['heartbeat', 'access'])
log_gen.run()
```

**Arguments**

* `out_path`: path of output logs

* `out_format`: format of output logs

* `mode`: log traffic mode

## License
See the LICENSE file for license rights and limitations (MIT).

