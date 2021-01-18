import sys
import os
import logging.config
from datetime import datetime
from os.path import abspath, dirname, join
from nav_automation.nav_handler import NavHandler
from nav_automation.constants import Constants

def main():
    # print command line arguments
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        logging.config.fileConfig( join(dirname(abspath(__file__)), "logging_config.ini")
									, defaults={'date':datetime.now().date().strftime('%Y-%m-%d')}
								)
		#-- 10 second timeout
		#-- fundName set as stbf
        NavHandler().run(filepath, Constants.MODE_TEST, 10, "stbf")
    else:
        print_menu()

def print_menu():
	print("To Run Program               : python -m nav_automation <workbook_filepath>")
	print("Sample Run                   : python -m nav_automation \"samples\\sample PriceSTBF.xls\" ")
	print("")
	print("To Run Unittest              : python -m unittest2")

if __name__ == "__main__":
    main()
