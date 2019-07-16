# -*- coding: utf-8 -*-
# python 2.x required.
from urllib2 import Request, urlopen
from urllib import urlencode, unquote, quote_plus
from HTMLParser import HTMLParser
import threading, datetime, sys
reload(sys)
sys.setdefaultencoding("utf-8")

unescape = HTMLParser().unescape	#  &lt; &gt; &amp; &nbsp; &quot; 등을 < > &  " 등으로 처리하기 위한 함수.

start_datetime = datetime.datetime.now()
print ("Starting " + str(start_datetime))

#생성될 파일명의 앞 부분을 정의함.
XML_filename_prefix = "Python_xmldownload_"
CVS_filename_prefix = "item_"

def xml2csv(key_value):

	print ("\nBeginning to Convert xml to csv for KEY: " + key_value + " || " + str(datetime.datetime.now()))
	xmlFile = open(XML_filename_prefix + key_value + ".xml", 'r')
	csvFile = open(CVS_filename_prefix + key_value + ".csv", 'w')
	csvFile.write('\xEF\xBB\xBF')	#엑셀에서 한글 인식 가능하도록... (UTF-8 BOM)
	item_no = 0						#To count total number of columns
	max_item_no = 0
	row_no = 0  					#To count total number of rows
	item_inside = False				#To determine if curernt line is in the item tag.
	columns = []
	row_content = ""
	for line in xmlFile.readlines():
		if not line: break
		if line.find("<item>") < 0 and not item_inside:
			continue
		elif not item_inside:
			item_inside = not item_inside
			row_no += 1
			continue
		else:
			if row_no > 1 and item_no > max_item_no:
				print ("This xml file is NOT regular")
				csvFile.write("This xml file NOT regular")
			if line.find("</item>") >= 0 and item_inside:
				item_no = 0
				if row_no == 1:
					for column in columns:
						if item_no > 0:
							csvFile.write(",")
						csvFile.write(column)
						item_no += 1
					item_no = 0
				csvFile.write('\n')
				csvFile.write(row_content)
				row_content = ""           
				max_item_no = len(columns)
				item_inside = not item_inside
				continue
			columns.append(line[line.find("<")+1:line.find(">")])
			line = line[line.find(">")+1:]
			line = line[:line.find("<")]
			line = unescape(line)
			line = line.replace("\"", "\"\"")
			if item_no > 0:
				row_content += "," 
			row_content += "\"" + line + "\""
			item_no += 1

	csvFile.close()
	xmlFile.close()

	print ("\nConverting xml to csv for KEY: " + key_value + " is done" + " || " + str(datetime.datetime.now()))


if __name__=='__main__':
	url = 'http://apis.data.go.kr/B553077/api/open/sdsc/storeListInUpjong'
	ServiceKey = 'w%2FwDcFR1uQOIVcsDzVkIUwqmjBMNuTjnKmvpC%2BnTdkeqes6V%2Fxc6BfcN%2BJBM51AK84fms61n0NYDr9jhv0i1Fg%3D%3D'
	divId = 'indsLclsCd'
	numOfRows = 1000

	key_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	### Below array is for simple test ###
	#key_array = ['O', 'P', 'L', 'M', 'N', 'Z']
	maxPageArray = []

	for key_value in key_array:

		queryParams = '?' + unquote(urlencode({ quote_plus('ServiceKey') : ServiceKey, quote_plus('key') : key_value, quote_plus('divId') : divId, quote_plus('numOfRows') : '1', quote_plus('pageNo') : '1' }))

		request = Request(url + queryParams)
		request.get_method = lambda: 'GET'
		response_body = urlopen(request)

		maxPageNo = 0
		for line in response_body.readlines():
			if "totalCount" in line:
				maxPageNo = int(line.strip().replace("<totalCount>","").replace("</totalCount>",""))

		if maxPageNo > 0:
			maxPageArray.append([key_value, maxPageNo])
		else:
			print ("No contents for KEY: " + key_value)

	for key_value in maxPageArray:
		print ("\nCollecting XML KEY: " + key_value[0] + "  // Total number of rows: " + str(key_value[1]))
		if key_value[1] % numOfRows > 0:
			key_value[1] = key_value[1] / numOfRows + 1
		else:
			key_value[1] = key_value[1] / numOfRows

		pageNo = 1
		while pageNo <= key_value[1]:
			queryParams = '?' + unquote(urlencode({ quote_plus('ServiceKey') : ServiceKey, quote_plus('key') : key_value[0], quote_plus('divId') : divId, quote_plus('numOfRows') : numOfRows, quote_plus('pageNo') : pageNo }))
			request = Request(url + queryParams)
			request.get_method = lambda: 'GET'
			response_body = urlopen(request).read()
			file_name = XML_filename_prefix + key_value[0] +".xml"
			if pageNo == 1:
				f = open(file_name, 'w')
			else:
				f = open(file_name, 'a')
			f.write(response_body)
			pageNo += 1
		print ("\nCompleted to Collect XML KEY: " + key_value[0] + " || " + str(datetime.datetime.now()))
		f.close()
		
		xml2cvs_thread = threading.Thread(target=xml2csv, args=key_value[0])
		xml2cvs_thread.start()

#	end_datetime = datetime.datetime.now()

#print ("\nStarting " + str(start_datetime))
#print ("\nEnding to collect XML " + str(end_datetime))
