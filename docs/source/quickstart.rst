.. _quickstart:

QuickStart
==========

Sometimes we want to quickly test our log monitor and analyzer, to see if they can perform correctly,but don't have log sources in hand. Lunaticlog gives you the ability to create fake log loads, which supports log rotation and content distribution control. It can also stress testing the system by generating traffic spikes.

Log Generating Summary
----------------------

Begin by importing a log generator module:

.. code-block:: python

	>>> from lunaticlog import apache_gen

Instantiate the generator and set the output path:

.. code-block:: python

	>>> log_gen = apache_gen(out_path='./apache.log')

Finally let it begin to generate logs:

.. code-block:: python

	>>> log_gen.run()

Now, we can check the output path that we set to see the generated logs.


Log Format Support
------------------

- Apache Access Log

.. code-block:: none

	127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326

- [TODO] Nginx Access Log

.. code-block:: none

	123.65.150.10 - - [23/Aug/2010:03:50:59 +0000] "POST /wordpress3/wp-admin/admin-ajax.php HTTP/1.1" 200 2 "http://www.example.com/wordpress3/wp-admin/post-new.php" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3"

- [TODO] Amazon S3 Log

.. code-block:: none

	79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be mybucket [06/Feb/2014:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /mybucket?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" -


Log Roatation
-------------

Set attribute ``rotation_size`` to rotate logs when current log file achieves the max size:

.. code-block:: none

	# content of file config/apache_gen.json
	"rotation_size": 10000

And turn on the log rotation when creating generator objects:

.. code-block:: none

	log_gen = apache_gen(out_path='./apache.log', rotation=True)


Log Field Content Distribution
------------------------------

Since we are trying to build a fake log generator to simulate a real cluster, we are eager to add as much randomness as possible to the generated logs, to make it look more similar to real ones.

To make them more realistic, we also want to fill in log fileds using contents with some given distributions.

For example, we may want to generate more ``GET`` messages than ``POST`` ones.

To configure the distributions, use Apache Access Log's HTTP method field as an example:

.. code-block:: none
	
	# content of config/apache_gen.json
	"methods": ["GET", "POST", "PUT", "DELETE"],
	"methods_p": [0.7,0.1,0.1,0.1],
	
``methods_p`` list configures the distributions of corresponding HTTP methods in list ``methods``.


Log Generation Mode
-------------------

Lunaticlogs can create chaos to help you stress test your system. Now it has 3 different log generation modes:


- Uniform Mode

	Generate logs at a random rate, which is uniformly distributed.

.. image:: https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_uniform.png
		:width: 320 px
		:height: 240 px
		:align: center

- Push Mode

	Generate logs at highest speed configured.

.. image:: https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_push.png
		:width: 320 px
		:height: 240 px
		:align: center

- Spike Mode

	Generate logs at sudden very high rates periodically.

.. image:: https://raw.githubusercontent.com/xuwenyihust/lunaticlog/master/img/mode_spike.png
		:width: 320 px
		:height: 240 px
		:align: center


Select the modes during generator instantiation:

.. code-block:: python

	log_gen = apache_gen(out_path='./apache.log', mode='uniform')




