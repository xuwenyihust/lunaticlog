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


Source Code
-----------

Features
--------

Documentation
-------------

License
-------
MIT License

Copyright (c) 2017 WenyiXu

.. _`MIT`: https://github.com/xuwenyihust/lunaticlog/blob/master/LICENSE

.. toctree::
   :maxdepth: 2

   getting-started

