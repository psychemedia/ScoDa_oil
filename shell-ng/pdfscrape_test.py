# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://s06.static-shell.com/content/dam/shell/static/nga/downloads/pdfs/oil-spills/864855_Opukush_Well_25_at_Agbediama.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
print "There are",len(pages),"pages"

# 6. Iterate through the elements in each page, and preview them
for page in pages:
    for el in page:
        if el.tag == "text":
            print el.text, el.attrib
