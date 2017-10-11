# -*- coding: UTF-8 -*-
from lxml import etree, html
import urllib2

sitemap_file = "url_list.xml"
site = etree.parse(sitemap_file).getroot()

globalCounter = 0
categoryCounter = 0
questionCounter = 0
contributionCounter = 0
selfCategory = False
selfQuestion = False


for category in site:
	if category.get("self") == "true":
		selfCategory = True
	else:
		selfCategory = False
	
	print 'Scanning category:', category.get("label")
	
	for question in category:
		if question.get("self") == "true":
			selfQuestion = True
		else:
			selfQuestion = False
		
		page = html.fromstring(urllib2.urlopen(question.get("url")).read())
		page
		for contribution in page.xpath('//div[@class="user-contribution block-content"]'):
			contributionCounter += 1

		
print ""		
print 'Total contributions:', contributionCounter
print ""
print 'Ranking of "R&D Hyperloop" topic:'
print '- In its sub-category: ', questionCounter
print '- In its category: ', categoryCounter
print "- In the whole site: ", globalCounter
print ""
raw_input("Press Enter to exit...")