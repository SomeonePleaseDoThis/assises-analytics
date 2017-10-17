# -*- coding: UTF-8 -*-
from lxml import etree, html
import urllib2

sitemap_file = "url_list.xml"
domain = "https://www.assisesdelamobilite.gouv.fr"
site = etree.parse(sitemap_file).getroot()

numberContributionGlobal = 1
numberContributionSelfCategory = 1
numberContributionSelfSubcategory = 1
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
bestScore = selfScore
nextScore = 0
print "Score of R&D Hyperloop:", selfScore
print ""


#Scan all contribution
for category in site:
	# Determine if this is the category of my topic
	if category.get("self") == "true":
		selfCategory = True
	else:
		selfCategory = False
	
	print 'Scanning category:', category.get("label")
	numberContributionThisCategory = 0
	
	for subcategory in category:
		#print "New subcategory"
		# Determine if this is the subcategory of my topic
		if subcategory.get("self") == "true":
			selfSubcategory = True
		else:
			selfSubcategory = False
		
		# Due to the fact that only 12 contributions are loaded per page, first page and next pages has to be handled differently.
		isFirstPageOfSubcategory = True
		hasContributions = True

		# Loop as long as subcategory batches has contributions
		while hasContributions:
			# Get page content
			if isFirstPageOfSubcategory:
				page = html.fromstring(urllib2.urlopen(subcategory.get("url")).read())
			else:
				#print additionalUrl
				
				ajaxRaw = urllib2.urlopen(additionalUrl).read()
				ajaxData = ajaxRaw.split('"data":"')
				
				encodedData = (ajaxData[1].split('"'))[0]
				# with open('encodedData.txt', 'w') as myFile:
					# myFile.write(encodedData)
					# myFile.close
				
				decodedData = encodedData.decode('unicode-escape')
				decodedData = decodedData.replace('\/', '/')
				decodedData = decodedData.replace('&', '')
				# with open('decodedData.txt', 'w') as myFile:
					# myFile.write(decodedData.encode('utf-8'))
					# myFile.close
					
				page = html.fromstring('<div>' + decodedData + '</div>')
				# with open('mypage.html', 'w') as myFile:
					# myFile.write(html.tostring(page))
					# myFile.close
		
			# Compute score
			for contribution in page.xpath('//div[@class = "user-contribution block-content" and @data-contrib != "' + id + '"]'):
				numberContributionGlobal += 1
				numberContributionThisCategory += 1 # is reset before scanning each category
				if selfCategory:
					numberContributionSelfCategory += 1
				if selfSubcategory:
					numberContributionSelfSubcategory += 1
				
				likeNode = contribution.xpath('.//div[@class="float-left like-count-entity-node"]')
				#print likeNode
				plusNumber = int(likeNode[0].text)
				#minusNumber = int(contribution.xpath('.//div[@class="float-left dislike-count-entity-node"]')[0].text)
				
				score = plusNumber
				#print score
				
				# Compute rankings and scores
				if score > selfScore:
					# Compute rankings
					selfRankGlobal +=1
					if selfCategory:
						selfRankCategory += 1
					if selfSubcategory:
						selfRankSubcategory += 1
						
					# Compute best score
					if score > bestScore:
						bestScore = score
						if nextScore == 0: # Initialization to the first best score
							nextScore = bestScore
					
					# Compute next score
					if score < nextScore:
						nextScore = score
					
				elif score == selfScore:
					selfExaequoGlobal +=1
					if selfCategory:
						selfExaequoCategory += 1
					if selfSubcategory:
						selfExaequoSubcategory += 1
			
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
	
	print " ->", numberContributionThisCategory, "contributions"
	
print ""		
print 'Ranking of "R&D Hyperloop" topic:'
print '- In its sub-category:', selfRankSubcategory, '/', numberContributionSelfSubcategory, '( Ex aequo:', selfExaequoSubcategory, ')'
print '- In its category:', selfRankCategory, '/', numberContributionSelfCategory, '( Ex aequo:', selfExaequoCategory, ')'
print '- In the whole site:', selfRankGlobal, '/', numberContributionGlobal, '( Ex aequo:', selfExaequoGlobal, ')'
print '- Best score:', bestScore
print '- Next score:', nextScore
print ""
raw_input("Press Enter to exit...")