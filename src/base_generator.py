import abc


#################################
##
##  Abstract Base Log Generator
##
#################################
class log_gen(metaclass=abc.ABCMeta):

	@abc.abstractproperty
	def lines(self):
		pass

	@abc.abstractproperty
	def methods(self):
		pass

	@abc.abstractproperty
	def methods_p(self):
		pass

	@abc.abstractproperty
	def mode(self):
		pass

	@abc.abstractproperty
	def out_format(self):
		pass

	@abc.abstractmethod
	def run(self):
		pass




