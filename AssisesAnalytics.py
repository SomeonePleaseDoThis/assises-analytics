# -*- coding: UTF-8 -*-
from lxml import etree, html
import urllib2

sitemap_file = "url_list.xml"
site = etree.parse(sitemap_file).getroot()

numberContributionGlobal = 1
numberContributionCategory = 1
numberContributionSubcategory = 1
selfRankGlobal = 1
selfRankCategory = 1
selfRankSubcategory = 1
selfExaequoGlobal = 0
selfExaequoCategory = 0
selfExaequoSubcategory = 0
selfCategory = False
selfSubcategory = False


# Get self contribution score
subcategory = site.xpath('//subcategory[@self="true"]')[0]
url = subcategory.get('url')
id = subcategory.get('self-contrib-id')

page = html.fromstring(urllib2.urlopen(subcategory.get("url")).read())
contribution = page.xpath('//div[@class = "user-contribution block-content" and @data-contrib = "' + id + '"]')[0]
plusNumber = int(contribution.xpath('.//div[@class="float-left like-count-entity-node"]')[0].text)
#minusNumber = contribution.xpath('.//div[@class="float-left dislike-count-entity-node"]')[0].text

selfScore = plusNumber
print "Score of R&D Hyperloop:", selfScore
print ""


#Scan all contribution
for category in site:
	if category.get("self") == "true":
		selfCategory = True
	else:
		selfCategory = False
	
	print 'Scanning category:', category.get("label")
	
	for subcategory in category:
		if subcategory.get("self") == "true":
			selfSubcategory = True
		else:
			selfSubcategory = False
		
		page = html.fromstring(urllib2.urlopen(subcategory.get("url")).read())
		for contribution in page.xpath('//div[@class = "user-contribution block-content" and @data-contrib != "' + id + '"]'):
			numberContributionGlobal += 1
			if selfCategory:
				numberContributionCategory += 1
			if selfSubcategory:
				numberContributionSubcategory += 1
			
			plusNumber = int(contribution.xpath('.//div[@class="float-left like-count-entity-node"]')[0].text)
			#minusNumber = int(contribution.xpath('.//div[@class="float-left dislike-count-entity-node"]')[0].text)
			
			score = plusNumber
			print score
			
			if score > selfScore:
				selfRankGlobal +=1
				if selfCategory:
					selfRankCategory += 1
				if selfSubcategory:
					selfRankSubcategory += 1
			elif score == selfScore:
				selfExaequoGlobal +=1
				if selfCategory:
					selfExaequoCategory += 1
				if selfSubcategory:
					selfExaequoSubcategory += 1
		
print ""		
print 'Ranking of "R&D Hyperloop" topic:'
print '- In its sub-category: ', selfRankSubcategory, '/', numberContributionSubcategory, '( Ex aequo:', selfExaequoSubcategory, ')'
print '- In its category: ', selfRankCategory, '/', numberContributionCategory, '( Ex aequo:', selfExaequoCategory, ')'
print "- In the whole site: ", selfRankGlobal, '/', numberContributionGlobal, '( Ex aequo:', selfExaequoGlobal, ')'
print ""
raw_input("Press Enter to exit...")