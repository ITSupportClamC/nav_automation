# coding=utf-8
#
# Functions needed to calculate IMA yield
# 
from os.path import abspath, dirname



def getSTBFNavDataFromFile(file):
	"""
	[String] file (daily NAV file for Short Term Bond Fund)
		=> [Iterable] ( date (yyyy-mm-dd)
					  , class
					  , currency
					  , number of unit
					  , total nav of the class
					  , nav per unit)
	"""
	# FIXME: to be implemented
	return []



def updateWebSite(mode, timeOut, fundName, navData):
	"""
	[String] mode (0 means production, 1 means test)
	[String] timeout (in miliseconds)
	[String] fund name,
	[Tuple] nav Data (date, class, currency, nav)

	In production mode (0), update the website in production.
	In test mode (1), update the test website.

	Web sites (production, test) and login credentials should be
	configurable in a file.

	If timed out when trying to update the web site, throw an exception.

	return 0 when successful, throw exception otherwise.
	"""
	# FIXME: to be implemented
	return 0



"""
	returns the current directory

	for running the test case provided
"""
getCurrentDirectory = lambda : \
	dirname(abspath(__file__))



