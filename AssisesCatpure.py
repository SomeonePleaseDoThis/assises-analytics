# -*- coding: UTF-8 -*-
from lxml import etree, html
import urllib2
import xlwt

sitemap_file = "url_list.xml"
domain = "https://www.assisesdelamobilite.gouv.fr"
site = etree.parse(sitemap_file).getroot()
wb = xlwt.Workbook(encoding="utf-8")
ws = wb.add_sheet("List")
xlRow = 0

#Scan all contribution
for category in site:
	categoryName = category.get("label")
	print 'Scanning category:', categoryName
	
	for question in category:
		questionName = question.get("name")
		print 'Scanning question:', questionName
		# Due to the fact that only 12 contributions are loaded per page, first page and next pages has to be handled differently.
		isFirstPageOfSubcategory = True
		hasContributions = True

		# Loop as long as question batches has contributions
		while hasContributions:
			# Get page content
			if isFirstPageOfSubcategory:
				page = html.fromstring(urllib2.urlopen(question.get("url")).read())
				print '-', question.get("url")
			else:
				ajaxRaw = urllib2.urlopen(additionalUrl).read()
				ajaxData = ajaxRaw.split('"data":"')
				encodedData = (ajaxData[1].split('"'))[0]
				decodedData = encodedData.decode('unicode-escape')
				decodedData = decodedData.replace('\/', '/')
				decodedData = decodedData.replace('&', '')
				page = html.fromstring('<div>' + decodedData + '</div>')
				
				print '-', additionalUrl
		
			# Capture data
			for contribution in page.xpath('//div[@class = "user-contribution block-content"]'):
				# Get contribution information
				title = contribution.xpath('.//a[@data-original-title]')[0].get('data-original-title')
				#print title
				date = contribution.xpath('.//span[@class="contrib-date date"]')[0].text
				text = contribution.xpath('.//div[@class="contrib-text"]')[0].text
				
				plusNumber = int(contribution.xpath('.//div[@class="float-left like-count-entity-node"]')[0].text)
				minusNumber = int(contribution.xpath('.//div[@class="float-left dislike-count-entity-node"]')[0].text)
				nbComments = int(contribution.xpath('.//li[@class="nb-comments"]/a/span')[0].text)
				
				# Write contribution information
				ws.write(xlRow, 0, categoryName)
				ws.write(xlRow, 1, questionName)
				ws.write(xlRow, 2, title)
				ws.write(xlRow, 3, date)
				ws.write(xlRow, 4, text)
				ws.write(xlRow, 5, plusNumber)
				ws.write(xlRow, 6, minusNumber)
				ws.write(xlRow, 7, nbComments)
				
				#  Get comments information
				if nbComments > 0:
					# Initialize Excel column
					xlColumn = 8
					
					# Get comment list
					for comment in contribution.xpath('.//div[starts-with(@class,"comment ")]'): # space after "comment" is important
						commentAuthor = comment.xpath('.//div[@class="author"]/span')[0].text
						commentDate = comment.xpath('.//div[@class="submitted"]/span')[0].text
						commentText = comment.xpath('.//div[@class="field-items"]/div')[0].text
						
						commentPlusNumber = int(comment.xpath('.//div[@class="float-left like-count-entity-comment"]')[0].text)
						commentMinusNumber = int(comment.xpath('.//div[@class="float-left dislike-count-entity-comment"]')[0].text)
					
						#  Write comment information
						ws.write(xlRow, xlColumn, commentAuthor)
						ws.write(xlRow, xlColumn+1, commentDate)
						ws.write(xlRow, xlColumn+2, commentText)
						ws.write(xlRow, xlColumn+3, commentPlusNumber)
						ws.write(xlRow, xlColumn+4, commentMinusNumber)
						
						# Increment Excel column for potential next comment
						xlColumn += 5
						
				# Increment Excel row for potential next contribution
				xlRow += 1
				
			# Check if page has a link to more contributions. If so, get url.
			hasContributions = False
			if isFirstPageOfSubcategory:
				ajaxLink = page.xpath('//a[@id="ajax-link"]')
				if len(ajaxLink) > 0:
					additionalUrl = domain + ajaxLink[0].get('href')
					hasContributions = True
			else:
				if len(ajaxData) > 2:
					encodedData = (ajaxData[2].split('"'))[0]
					decodedData = encodedData.decode('unicode-escape')
					decodedData = decodedData.replace('\/', '/')
					page = html.fromstring('<div>' + decodedData + '</div>')
					ajaxLink = page.xpath('//a[@id="ajax-link"]')
					additionalUrl = domain + ajaxLink[0].get('href')
					hasContributions = True
			
			# Set to false after first pass
			isFirstPageOfSubcategory = False
		
wb.save('AssisesMobilitePlateformeCatpure.xls')
raw_input("Press Enter to exit...")