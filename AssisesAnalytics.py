# -*- coding: UTF-8 -*-
from lxml import etree

sitemap_file = "url_list.xml"
site = etree.parse(sitemap_file).getroot()

globalCounter = 0
categoryCounter = 0
questionCounter = 0
selfCategory = False
selfQuestion = False


for category in site:
	if category.get("self") == "true":
		selfCategory = True
	else:
		selfCategory = False
	
	for question in category:
		if question.get("self") == "true":
			selfQuestion = True
		else:
			selfQuestion = False

print "Classement du sujet R&D Hyperloop"
print "- Dans sa sous-catégorie: ", questionCounter
print "- Dans sa catégorie: ", categoryCounter
print "- Au global: ", globalCounter
print ""
raw_input("Press Enter to exit...")