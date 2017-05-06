# Lunatic
Log loads generator, test if your system can survive under the log spikes.

## Supported Log Format
What kinds of log formats does it support now?

* Apache Access Log

`127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326`


## Usage

* Install the dependencies

`pip install -r requirements.txt`


## Parameters

* `-m` The log generator mode, which log format to generate.

* `-o` The output log file path.

