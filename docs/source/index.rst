.. _toc:

lunaticlog: Fake log generator
==============================

Lunaticlog is a mock HTTP log generator package, use it's fake log workloads to test if your monitor / analyzer can survive various extreme conditions.

A simple usage example:

.. code-block:: python

	#content of test_sample.py

	from lunaticlog import apache_gen

	log_gen = apache_gen(out_path='./apache.log', mode='uniform', rotation=True)

	log_gen.run()

.. code-block:: none
	
	127.0.0.1 user-identifier frank [1/Oct/2017:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
	127.0.0.1 user-identifier james [1/Oct/2017:13:55:37 -0700] "POST /README.txt HTTP/1.0" 200 2326
	127.0.0.1 user-identifier putin [1/Oct/2017:13:55:38 -0700] "GET /image/cat.gif HTTP/1.0" 200 2326


Source Code
-----------

Get the `source code
<https://github.com/xuwenyihust/lunaticlog/>`_.

Features
--------

- Generate log in Apache Access format, Nginx format [TODO], AWS S3 format [TODO]

- Log file rotation configurable 

- Can control the distributions of log fields contents

- Different log generation mode for stress testing

- Python3.4, Python3.5, Python3.6

Documentation
-------------

For full documentation, including installation, tutorials and PDF documents, please see https://xuwenyihust.github.io/lunaticlog/lunaticlog/html/.

License
-------
`MIT
<https://github.com/xuwenyihust/lunaticlog/blob/master/LICENSE>`_ License

Copyright (c) 2017 WenyiXu

.. toctree::
   :maxdepth: 2

   installation

   quickstart

   contact

   license

   

  


