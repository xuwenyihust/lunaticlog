.. _quickstart:

QuickStart
==========

Sometimes we want to quickly test our log monitor and analyzer, to see if they can perform correctly,but don't have log sources in hand. Lunatilog gives you the ability to create fake log loads, which supports log rotation and content distribution control. It can also stress testing the system by generating traffic spikes.

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




Log Generation Mode
-------------------
