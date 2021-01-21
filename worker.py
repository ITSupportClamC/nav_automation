# coding=utf-8
#
# all the scheduling job starts from here.
# 
from nav_automation.nav_handler import getSTBFNavDataFromFile \
									, createBloombergExcelFile \
									, createThomsonExcelFile \
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



def doBloombergUpdate(templateFile, outputDir, data):
	"""
	[String] Bloomberg template file,
	[String] output directory,
	[List] fund data 
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	logger.debug('doBloombergUpdate()')
	try:
		file = createBloombergExcelFile( templateFile, outputDir
									   , 'stbf', data)

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



def doThomsonUpdate(templateFile, outputDir, data):
	"""
	[String] Thomson Reuters template file,
	[String] output directory,
	[List] fund data 
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	logger.debug('doThomsonUpdate()')
	try:
		file = createThomsonExcelFile( templateFile, outputDir
									 , 'stbf', data)

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



def sendNotificationEmail(fundName, status, message):
	"""
	[Int] status, [String] message

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



def processStbfInputFiles(files):
	"""
	[List] short term bond files (assume non-empty list)
		=> [Tuple] (status, message)
	"""
	if len(files) > 1:
		logger.error('handleStbfReport(): too many input files')
		return (Constants.STATUS_FAILURE, 'too many input files')

	data = list(getSTBFNavDataFromFile(files[0]))
	if len(data) == 0:
		logger.error('no data from {0}'.format(file))
		return (Constants.STATUS_FAILURE, 'failed to retrieve data')

	status01, message01 = doBloombergUpdate( getBloombergTemplateFile(getStbfDataDirectory())
									   	   , getStbfOutputDirectory()
									   	   , data)
	
	status02, message02 = doThomsonUpdate( getThomsonTemplateFile(getStbfDataDirectory())
										 , getStbfOutputDirectory()
										 , data)

	if (status01, status02) == (Constants.STATUS_SUCCESS, Constants.STATUS_SUCCESS):
		return (Constants.STATUS_SUCCESS, message01 + '\n' + message02)

	else:
		return (Constants.STATUS_FAILURE, message01 + '\n' + message02)



def moveFiles(outputDir, files):
	"""
	[String] output directory,
	[List] files (with full path)

	Side effect: move files to the output directory
	"""
	for fn in files:
		shutil.move(fn, join(outputDir, getFilenameWithoutPath(fn)))



def handleStbfReport():
	"""
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

	status, message = processStbfInputFiles(files)
	sendNotificationEmail('Short Term Bond Fund', status, message)
	moveFiles(getStbfProcessedDirectory(), files)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)

	import configparser
	from os.path import join
	config = configparser.ConfigParser()
	config.read(join(getCurrentDirectory(), 'nav_automation.config'))

	handleStbfReport()
	