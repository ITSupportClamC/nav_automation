# coding=utf-8
#
# all the scheduling job starts from here.
# 
from nav_automation.nav_handler import getSTBFNavDataFromFile \
									, createBloombergExcelFile \
									, createThomsonExcelFile \
									, updateWebSite \
									, getCurrentDirectory
from nav_automation.constants import Constants
from steven_utils.mail import sendMailWithAttachment, sendMail
from steven_utils.file import getFiles, getFilenameWithoutPath
from toolz.functoolz import compose
from functools import partial
import shutil
import logging
logger = logging.getLogger(__name__)



# [String] date (yyyy-mm-dd) => [String] email subject
getSubject = compose(
	lambda s: 'China Life Franklin Global Fund - Short Term Bond Fund as at ' + s
  , lambda L: L[1] + '/' + L[2] + '/' + L[0]
  , lambda date: date.split('-')
)



# [List] data => [String] date (yyyy-mm-dd)
getDateFromFunddata = lambda data: data[0][0]



def doBloombergUpdate(templateFile, outputDir, fundName, data):
	"""
	[String] Bloomberg template file,
	[String] output directory,
	[String] fund name,
	[List] fund data 
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	logger.debug('doBloombergUpdate()')
	try:
		file = createBloombergExcelFile( templateFile, outputDir
									   , fundName, data)

		sendMailWithAttachment( '', file
							  , getSubject(getDateFromFunddata(data))
							  , getMailSender()
						  	  , getBloombergMailRecipients()
						  	  , getMailServer()
						  	  , getMailTimeout())

		return (Constants.STATUS_SUCCESS, 'Bloomberg update succesful')

	except:
		logger.exception('doBloombergUpdate():')
		return (Constants.STATUS_FAILURE, 'Bloomberg update failed')



def doThomsonUpdate(templateFile, outputDir, fundName, data):
	"""
	[String] Thomson Reuters template file,
	[String] output directory,
	[String] fund name,
	[List] fund data 
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	logger.debug('doThomsonUpdate()')
	try:
		file = createThomsonExcelFile( templateFile, outputDir
									 , fundName, data)

		sendMailWithAttachment( '', file
							  , getSubject(getDateFromFunddata(data))
							  , getMailSender()
						  	  , getThomsonMailRecipients()
						  	  , getMailServer()
						  	  , getMailTimeout())

		return (Constants.STATUS_SUCCESS, 'Thomson Reuters update succesful')

	except:
		logger.exception('doThomsonUpdate():')
		return (Constants.STATUS_FAILURE, 'Thomson Reuters update failed')



def doWebsiteUpdate(mode, timeOut, fundName, data):
	"""
	[String] running mode (test or production)
	[Int] time out (in miliseconds)
	[String] fund name
	[Iterable] data to upload
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	logger.debug('doWebsiteUpdate()')
	try:
		for d in data:
			updateWebSite(mode, timeOut, fundName, d)

	except:
		logger.exception('doWebsiteUpdate():')
		return (Constants.STATUS_FAILURE, 'website update failed')


	return (Constants.STATUS_SUCCESS, 'website update succesful')



def sendNotificationEmail(fundName, status, message):
	"""
	[String] fund name, [Int] status, [String] message

	send email to notify the status. 
	"""
	getSubject = lambda fundName, status: \
		fundName + ' auto update succesful' \
		if status == Constants.STATUS_SUCCESS else \
		fundName + ' auto update failed'

	logger.debug('sendNotificationEmail(): {0}'.format(fundName))
	sendMail( message
			, getSubject(fundName, status)
			, getMailSender()
			, getNotificationMailRecipients()
			, getMailServer()
			, getMailTimeout())



def getMailSender():
	global config
	return config['email']['sender']



def getMailServer():
	global config
	return config['email']['server']



def getMailTimeout():
	global config
	return float(config['email']['timeout'])



def getBloombergMailRecipients():
	global config
	return config['email']['bloombergMailRecipients']



def getThomsonMailRecipients():
	global config
	return config['email']['thomsonMailRecipients']



def getNotificationMailRecipients():
	global config
	return config['email']['notificationMailRecipients']



def getBloombergTemplateFile(directory):
	global config
	return join(directory, config['email']['bloombergTemplateFile'])



def getThomsonTemplateFile(directory):
	global config
	return join(directory, config['email']['thomsonTemplateFile'])



def getStbfDataDirectory():
	global config
	return config['stbf']['dataDirectory']



def getStbfOutputDirectory():
	global config
	return config['stbf']['outputDirectory']



def getStbfProcessedDirectory():
	global config
	return config['stbf']['processed']



def getWebsiteTimeout():
	global config
	return int(config['web']['timeOut'])



def getStbfFilesFromDirectory(directory):
	"""
	[String] directory => [List] short term bond files under the dir
	"""
	isStbfFile = compose(
		lambda fn: fn.startswith('PriceSTBF') and fn.endswith('.xls')
	  , getFilenameWithoutPath
	)

	return \
	compose(
		list
	  , partial(filter, isStbfFile)
	  , lambda directory: getFiles(directory, withDir=True)
	)(directory)



def processStbfInputFiles(fundName, mode, files):
	"""
	[String] fund name
	[String] mode (production or test)
	[List] short term bond files (assume non-empty list)
		=> [Tuple] (status, message)

	This function should not throw exceptions.
	"""

	"""
	[Iterable] ( date, class, currency, number of unit
			   , total nav of the class, nav per unit)
	=> 
	[Iterable] (date, class, currency, nav per unit)
	"""
	if len(files) > 1:
		logger.error('processStbfInputFiles(): too many input files')
		return (Constants.STATUS_FAILURE, 'too many input files')

	try:
		data = list(getSTBFNavDataFromFile(files[0]))
		if len(data) == 0:
			logger.error('processStbfInputFiles(): empty data set: {0}'.format(files[0]))
			return (Constants.STATUS_FAILURE, 'empty data set')

	except:
		logger.exception('processStbfInputFiles()')
		return (Constants.STATUS_FAILURE, 'failed to retrieve data from file')


	status01, message01 = doBloombergUpdate( getBloombergTemplateFile(getStbfDataDirectory())
									   	   , getStbfOutputDirectory()
									   	   , fundName
									   	   , data)
	
	status02, message02 = doThomsonUpdate( getThomsonTemplateFile(getStbfDataDirectory())
										 , getStbfOutputDirectory()
										 , fundName
										 , data)

	status03, message03 = doWebsiteUpdate( mode
										 , getWebsiteTimeout()
										 , fundName
										 , data)


	if (status01, status02, status03) == \
		(Constants.STATUS_SUCCESS, Constants.STATUS_SUCCESS, Constants.STATUS_SUCCESS):
		return (Constants.STATUS_SUCCESS, message01 + '\n' + message02 + '\n' + message03)

	else:
		return (Constants.STATUS_FAILURE, message01 + '\n' + message02 + '\n' + message03)



def moveFiles(outputDir, files):
	"""
	[String] output directory,
	[List] files (with full path)

	Side effect: move files to the output directory
	"""
	for fn in files:
		shutil.move(fn, join(outputDir, getFilenameWithoutPath(fn)))



def handleStbfReport(fundName, mode):
	"""
	[String] fund name
	[String] mode (test or production)

	For period run purpose:

	1. read directory for input files;
	2. if no input files are found, do nothing;
	3. process input files and get status;
	4. send notification email.
	5. move input files to processed directory
	"""
	logger.debug('handleStbfReport()')
	files = list(getStbfFilesFromDirectory(getStbfDataDirectory()))
	if len(files) == 0:
		logger.debug('handleStbfReport(): no input files')
		return

	status, message = processStbfInputFiles(fundName, mode, files)
	sendNotificationEmail('Short Term Bond Fund', status, message)
	moveFiles(getStbfProcessedDirectory(), files)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)

	import configparser
	from os.path import join
	config = configparser.ConfigParser()
	config.read(join(getCurrentDirectory(), 'nav_automation.config'))

	"""
	To run the program in test mode, which means test web site will be
	updated, do (change stbf to other fund name if needed):

	$ python stbf

	To run the program in production mode:

	$ python stbf --production
	"""
	import argparse
	parser = argparse.ArgumentParser(description='NAV upload automation')
	parser.add_argument( 'fund', metavar='fund', type=str
					   , help='for which fund (stbf etc.)')
	parser.add_argument( '--production', type=bool, nargs='?', const=True, default=False
					   , help='run in production mode or test mode')
	args = parser.parse_args()
	mode = Constants.MODE_PRODUCTION if args.production else Constants.MODE_TEST
	fundName = args.fund


	import sys
	if not fundName in ('stbf',):
		logger.error('main(): invalid fundName: {0}'.format(fundName))
		sys.exit(1)

	if fundName == 'stbf':
		handleStbfReport(fundName, mode)
	