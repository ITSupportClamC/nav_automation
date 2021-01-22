import os

class Constants:
	#-- API Path
	MODE_TEST = 0
	MODE_PRODUCTION =  1
	API_TOKEN_STR = "clamc-website-api"
	API_TEST = "http://18.167.24.166/action/webservices/api/products/addnav"
	API_PRD = "https://clamc.com.hk/action/webservices/api/products/addnav"

	#-- bloomberg fund pricing worksheet column
	BG_COL_DATE = 1
	BG_COL_BLOOMBERG_CODE = 2
	BG_COL_FUND_NAME = 3
	BG_COL_CURRENCY = 4
	BG_COL_NAV = 5
	BG_COL_BID = 6
	BG_COL_OFFER = 7 
	BG_COL_FUND_SIZE_ACTUAL = 8
	BG_COL_CLASS_ASSETS_ACTUAL = 9
	BG_COL_SHARE_OUT_ACTUAL = 10
	BG_COL_FIRM_ASSETS_UNDER_MANAGEMENT_ACTUAL = 11

	#-- Thomson Reuters fund pricing worksheet column
	RE_COL_ISIN_CODE = 1
	RE_COL_NAME = 2
	RE_COL_CURRENCY = 3
	RE_COL_NAV_PER_SHARE = 4
	RE_COL_FUND_SIZE = 5
	RE_COL_CLASS_ASSETS = 6
	RE_COL_SHARE_OUT = 7

	#-- run status from periodic run
	STATUS_SUCCESS = 0
	STATUS_FAILURE = -1