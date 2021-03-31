import unittest2
from nav_automation.nav_handler import getCurrentDirectory \
									, getSTBFNavDataFromFile \
									, createBloombergExcelFile \
									, createThomsonExcelFile
from steven_utils.excel import fileToLines, getRawPositionsFromLines
from steven_utils.iter import skipN
from toolz.functoolz import compose
from functools import partial
from os.path import join



class TestNavHandlerSteven(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestNavHandlerSteven, self).__init__(*args, **kwargs)


	def testGetSTBFNavDataFromFile(self):
		file = join(getCurrentDirectory(), 'samples', 'sample PriceSTBF.xls')
		data = getSTBFNavDataFromFile(file)
		sortedData = sorted(data, key=lambda t: t[1])
		self.assertEqual(2, len(sortedData))
		self.assertEqual(
			('2020-12-30', 'Class B', 'USD', 400000, 3998441.60, 9.9961)
		  , sortedData[0]
		)
		self.assertEqual(
			('2020-12-30', 'Class I', 'USD', 4500000, 44981729.87, 9.9959)
		  , sortedData[1]
		)



	def testGetSTBFNavDataFromFile2(self):
		file = join(getCurrentDirectory(), 'samples', 'PriceSTBF 2021-01-15.xls')
		data = getSTBFNavDataFromFile(file)
		sortedData = sorted(data, key=lambda t: t[1])
		self.assertEqual(2, len(sortedData))
		self.assertEqual(
			('2021-01-15', 'Class B', 'USD', 400000, 3995663.95, 9.9891)
		  , sortedData[0]
		)
		self.assertEqual(
			('2021-01-15', 'Class I', 'USD', 24521823.7879, 244916195.05, 9.9876)
		  , sortedData[1]
		)



	def testCreateThomsonExcelFile(self):
		file = join(getCurrentDirectory(), 'samples', 'PriceSTBF 2021-01-19.xls')
		template = join( getCurrentDirectory(), 'samples'
					   , 'Thomson Reuters fund pricing template.xlsx')
		outputFile = createThomsonExcelFile( template, getCurrentDirectory()
										   , 'stbf', getSTBFNavDataFromFile(file))
		positions = compose(
			lambda L: sorted(L, key=lambda p: p['Name'])
		  , getRawPositionsFromLines
		  , fileToLines
		)(outputFile)

		self.assertEqual(2, len(positions))
		self.verififyThomsonPosition1(positions[0])
		self.verififyThomsonPosition2(positions[1])



	def testCreateThomsonExcelFile2(self):
		file = join(getCurrentDirectory(), 'samples', 'PriceSTBF 2021-03-30.xls')
		template = join( getCurrentDirectory(), 'samples'
					   , 'Thomson Reuters fund pricing template.xlsx')
		outputFile = createThomsonExcelFile( template, getCurrentDirectory()
										   , 'stbf', getSTBFNavDataFromFile(file))
		positions = compose(
			lambda L: sorted(L, key=lambda p: p['Name'])
		  , getRawPositionsFromLines
		  , fileToLines
		)(outputFile)

		self.assertEqual(3, len(positions))



	def testCreateBloombergExcelFile(self):
		file = join(getCurrentDirectory(), 'samples', 'PriceSTBF 2021-01-19.xls')
		template = join( getCurrentDirectory(), 'samples'
					   , 'Bloomberg fund pricing template.xlsx')
		outputFile = createBloombergExcelFile( template, getCurrentDirectory()
										   	 , 'stbf', getSTBFNavDataFromFile(file))
		positions = compose(
			lambda L: sorted(L, key=lambda p: p['FUND NAME'])
		  , getRawPositionsFromLines
		  , partial(skipN, 7)
		  , fileToLines
		)(outputFile)

		self.assertEqual(2, len(positions))
		self.verififyBloombergPosition1(positions[0])
		self.verififyBloombergPosition2(positions[1])



	def testCreateBloombergExcelFile2(self):
		file = join(getCurrentDirectory(), 'samples', 'PriceSTBF 2021-03-30.xls')
		template = join( getCurrentDirectory(), 'samples'
					   , 'Bloomberg fund pricing template.xlsx')
		outputFile = createBloombergExcelFile( template, getCurrentDirectory()
										   	 , 'stbf', getSTBFNavDataFromFile(file))
		positions = compose(
			lambda L: sorted(L, key=lambda p: p['FUND NAME'])
		  , getRawPositionsFromLines
		  , partial(skipN, 7)
		  , fileToLines
		)(outputFile)

		self.assertEqual(3, len(positions))



	def verififyThomsonPosition1(self, position):
		self.assertEqual(7, len(position))
		self.assertEqual('HK0000664455', position['ISIN Code'])
		self.assertEqual('China Life Franklin Global-Short Term Bond B USD', position['Name'])
		self.assertEqual('USD', position['Currency'])
		self.assertEqual(9.9914, position['NAV per share'])
		self.assertEqual(248960963.93, position['Fund Size'])
		self.assertEqual(3996581.49, position['Class Assets'])
		self.assertEqual(400000, position['Shares Outstanding'])



	def verififyThomsonPosition2(self, position):
		self.assertEqual(7, len(position))
		self.assertEqual('HK0000664489', position['ISIN Code'])
		self.assertEqual('China Life Franklin Global-Short Term Bond I USD', position['Name'])
		self.assertEqual('USD', position['Currency'])
		self.assertEqual(9.9896, position['NAV per share'])
		self.assertEqual(248960963.93, position['Fund Size'])
		self.assertEqual(244964382.44, position['Class Assets'])
		self.assertEqual(24521823.7879, position['Shares Outstanding'])



	def verififyBloombergPosition1(self, position):
		self.assertEqual(11, len(position))
		self.assertEqual('01/19/2021', position['DATE (MM/DD/YYYY)'])
		self.assertEqual('CLSTFBU HK Equity', position['BLOOMBERG CODE / ISIN / SEDOL'])
		self.assertEqual('CHINA LIFE FR ST BOND-B USD', position['FUND NAME'])
		self.assertEqual('USD', position['CURRENCY'])
		self.assertEqual(9.9914, position['NAV'])
		self.assertEqual('', position['BID'])
		self.assertEqual('', position['OFFER'])
		self.assertEqual(248960963.93, position['FUND SIZE (Actual)'])
		self.assertEqual(3996581.49, position['CLASS ASSETS (Actual)'])
		self.assertEqual(400000, position['SHARE OUT (Actual)'])
		self.assertEqual('', position['FIRM ASSETS UNDER MANAGEMENT (Actual)'])



	def verififyBloombergPosition2(self, position):
		self.assertEqual(11, len(position))
		self.assertEqual('01/19/2021', position['DATE (MM/DD/YYYY)'])
		self.assertEqual('CLSTFIU HK Equity', position['BLOOMBERG CODE / ISIN / SEDOL'])
		self.assertEqual('CHINA LIFE FR ST BOND-I USD', position['FUND NAME'])
		self.assertEqual('USD', position['CURRENCY'])
		self.assertEqual(9.9896, position['NAV'])
		self.assertEqual('', position['BID'])
		self.assertEqual('', position['OFFER'])
		self.assertEqual(248960963.93, position['FUND SIZE (Actual)'])
		self.assertEqual(244964382.44, position['CLASS ASSETS (Actual)'])
		self.assertEqual(24521823.7879, position['SHARE OUT (Actual)'])
		self.assertEqual('', position['FIRM ASSETS UNDER MANAGEMENT (Actual)'])
