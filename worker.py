# coding=utf-8
#
# all the scheduling job starts from here.
# 
from nav_automation.nav_handler import getSTBFNavDataFromFile \
									, createBloombergExcelFile \
									, getCurrentDirectory
from nav_automation.constants import Constants
from steven_utils.mail import sendMailWithAttachment
from steven_utils.file import getFiles
from toolz.functoolz import compose

import logging
logger = logging.getLogger(__name__)



# [String] date (yyyy-mm-dd) => [String] email subject
getSubject = compose(
	lambda s: 'China Life Franklin Global Fund - Short Term Bond Fund as at ' + s
  , lambda L: L[1] + '/' + L[2] + '/' + L[0]
  , lambda date: date.split('-')
)



def sendBloombergNotification(date, file):
	"""
	[String] date (yyyy-mm-dd),
	[String] attachment file
	"""
	logger.debug('sendBloombergNotification(): {0}'.format(date))
	sendMailWithAttachment( '', file, getSubject(date), getMailSender()
						  , getBlpMailRecipients(), getMailServer(), getMailTimeout())



def processStbfFileForBlpThomson( blpTemplateFile, thomsonTemplateFile \
								, outputDir, file):
	"""
	[String] Bloomberg template file,
	[String] Thomson Reuters template file,
	[String] output directory,
	[String] input file 
		=> [Tuple] ([Int] result, [String] message)

	This function does not throw any exceptions.
	"""
	# [List] data => [String] date (yyyy-mm-dd)
	getDateFromData = lambda data: data[0][0]


	logger.debug('processFile(): {0}'.format(file))
	try:
		data = list(getSTBFNavDataFromFile(file))
		if len(data) == 0:
			return (Constants.STATUS_WARNING, 'no data from {0}'.format(file))

		excelFile = createBloombergExcelFile( blpTemplateFile, outputDir
											, 'stbf', data)

		sendBloombergNotification(getDateFromData(data), excelFile)

		return (Constants.STATUS_SUCCESS, '')

	except:
		logger.exception('processFile():')
		return (Constants.STATUS_FAILURE, '')



def getMailSender():
	global config
	return config['email']['sender']



def getMailServer():
	global config
	return config['email']['server']



def getMailTimeout():
	global config
	return float(config['email']['timeout'])



def getBlpMailRecipients():
	global config
	return config['email']['blpMailRecipients']



def getDataDirectory():
	global config
	return config['email']['dataDirectory']



def handleReport():
	"""
	For period run purpose:

	1. read directory for input file
	2. if no file, log and exit;
	3. if there are files, process it and get processing status;
	4. send notification email.

	"""
	logger.debug('handleReport()')
	




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)

	
	import configparser
	from os.path import join
	config = configparser.ConfigParser()
	config.read(join(getCurrentDirectory(), 'nav_automation.config'))

	import sys
	