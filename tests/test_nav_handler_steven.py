import unittest2
from nav_automation.nav_handler import getCurrentDirectory \
									, getSTBFNavDataFromFile
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