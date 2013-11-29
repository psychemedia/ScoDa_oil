import os,re
import urllib2

import pandas as pd

#url='http://s01.static-shell.com/content/dam/shell-new/local/country/nga/downloads/pdf/oil-spills/967426_BenisedeWell11_flowline_at_Amabulou_Photos.pdf'

df= pd.read_csv('shell_30_11_13_ng.csv')

errors=[]

for url in df[df.columns[15]]:
	try:
		print 'trying',url
		u = urllib2.urlopen(url)
		fn=url.split('/')[-1]

		localFile = open(fn, 'w')
		localFile.write(u.read())
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
	cmd=' '.join(['pdfimages -j',fn, idp, '; mv',fn,fo  ])
	os.system(cmd)
	#Still a couple of errors on filenames
	#just as quick to catch by hand/inspection of files that don't get moved properly
	
print 'Errors',errors