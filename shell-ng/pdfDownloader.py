import os,re
import urllib2

import pandas as pd


import scraperwiki
import urllib2, lxml.etree


def pdfParser(pdfdata,path):
	txt=[]
	
	pdfdata = urllib2.urlopen(url).read()
	xmldata = scraperwiki.pdftoxml(pdfdata)
	root = lxml.etree.fromstring(xmldata)

	# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
	#print lxml.etree.tostring(root, pretty_print=True)

	# 5. How many pages in the PDF document?
	pages = list(root)
	#print "There are",len(pages),"pages"

	# 6. Iterate through the elements in each page, and preview them
	for page in pages:
		for el in page:
			if el.tag == "text":
				#print el.text, el.attrib
				if el.text!=None: txt.append(el.text)


	try:
		ftxt=open(path+'/text.txt','w')
		ftxt.write("\n".join(txt).encode('utf-8'))
		ftxt.close()
	except: pass
            
#url='http://s01.static-shell.com/content/dam/shell-new/local/country/nga/downloads/pdf/oil-spills/967426_BenisedeWell11_flowline_at_Amabulou_Photos.pdf'

df= pd.read_csv('shell_30_11_13_ng.csv')

errors=[]

for url in df[df.columns[15]]:
	try:
		print 'trying',url
		u = urllib2.urlopen(url)
		fn=url.split('/')[-1]
		pdfdata=u.read()
		localFile = open(fn, 'w')
		localFile.write(pdfdata)
		localFile.close()
	except:
		print 'error with',url
		errors.append(url)
		continue
	
	#id= fn.split('_')[0]
	id=re.split(r'[_-]',fn)[0]
	fo='data/'+id
	os.system(' '.join(['mkdir',fo]))
	idp='/'.join([fo,id])
	
	fn= re.sub(r'([()&])', r'\\\1', fn)
	#http://ubuntugenius.wordpress.com/2012/02/04/how-to-extract-images-from-pdf-documents-in-ubuntulinux/ poppler-utils
	cmd=' '.join(['pdfimages -j',fn, idp, '; mv',fn,fo  ])
	os.system(cmd)
	#Still a couple of errors on filenames
	#just as quick to catch by hand/inspection of files that don't get moved properly
	
	pdfParser(pdfdata,fo)
	
print 'Errors',errors