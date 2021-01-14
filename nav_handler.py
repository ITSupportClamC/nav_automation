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



def createBloombergExcelFile(templateFile, outputDir, fundName, data):
	"""
	[String] template file,
	[String] output directory,
	[String] fund name
	[Iterable] ( date (yyyy-mm-dd)
			   , class
			   , currency
			   , number of unit
			   , total nav of the class
			   , nav per unit)

	=> [String] output file

	Assume: the list of classes in data all belong to the same fund.

	Side effect: create an excel file in the output directory,
	with the data populated. The template file should be kept
	unchanged.
	"""
	# FIXME: add implementation
	return ''



def createThomsonExcelFile(templateFile, outputDir, fundName, data):
	"""
	[String] template file,
	[String] output directory,
	[String] fund name
	[Iterable] ( date (yyyy-mm-dd)
			   , class
			   , currency
			   , number of unit
			   , total nav of the class
			   , nav per unit)

	=> [String] output file

	Assume: the list of classes in data all belong to the same fund.

	Side effect: create an excel file in the output directory,
	with the data populated. The template file should be kept
	unchanged.
	"""
	# FIXME: add implementation
	return ''



def getBloombergCode(fundName, className, currency):
	"""
	[String] fund name,
	[String] class name,
	[String] currency
		=> [String] Bloomberg code
	"""
	f_map = \
	{ ('stbf', 'Class B', 'USD'): 'CLSTFBU HK Equity'
	, ('stbf', 'Class I', 'USD'): 'CLSTFIU HK Equity'
	}
	return f_map[(fundName, className, currency)]



def getBloombergFundname(fundName):
	"""
	"""
	f_map = {'stbf': 'CHINA LIFE FR ST BOND'}
	return f_map[fundName]



def getThomsonReutersFundname(fundName):
	"""
	[String] fund name,
	[String] class name
		=> [Tuple] ISIN code, Thomson Reuters fund name
	"""
	f_map = {'stbf': 'China Life Franklin Global-Short Term Bond'}
	return f_map[fundName]



def getISINCode(fundName, className):
	"""
	[String] fund name,
	[String] class name
		=> [String] ISIN code
	"""
	f_map = \
	{ ('stbf', 'Class B'): 'HK0000664455'
	, ('stbf', 'Class I'): 'HK0000664489'
	}
	return f_map[(fundName, className)]



"""
	returns the current directory

	for running the test case provided
"""
getCurrentDirectory = lambda : \
	dirname(abspath(__file__))
