from BeautifulSoup import BeautifulSoup
import sys, os, re

def usage():
	return "scraper.py wikifile"

def parseCode(code):
	match = re.search(r"(\d)ALH(\d\d)", code).groups()
	return (match[0], match[1])

def scrape(inStream):
	soup = BeautifulSoup(inStream)
	rows = [f.parent for f in soup('td', {'class' : 'summary'})]

	epsAndNames = {}

	for row in rows:
		cells = row.findAll('td')
		if len(cells) < 7: 
			continue

		seasonEp = parseCode(cells[7].contents[0])
		season = int(seasonEp[0])
		ep = int(seasonEp[1])

		if cells[2].b.a :
			name = cells[2].b.a.contents[0]
		elif cells[2].b:
			name = cells[2].b.contents[0]
		else:
			continue

		if not epsAndNames.has_key(season):
			epsAndNames[season] = {}
		
		epsAndNames[season][ep] = name
		
	return epsAndNames

def main():
	if len(sys.argv) != 2:
		print usage()
		sys.exit()
	
	print scrape(open(sys.argv[1]))[1]

if __name__ == '__main__':
	main()