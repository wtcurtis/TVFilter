import sys, os, re, scraper

def renameAll(rootDir, metadataFile):
	try:
		season = os.path.basename(rootDir)
		metadata = scraper.scrape(open(metadataFile))
		metadata
	#	print metadata
	#	sys.exit()
	
	except ValueError:
		print "Couldn't parse the season from the given."
		return 0
	
	files = os.listdir(rootDir)

	parsedFiles = []
	pattern = re.compile(r"([\w ]*) - (\d\d)x(\d\d)(.*)")

	for f in files:
		matches = pattern.search(f).groups()
		orgFile = os.path.join(rootDir, f)
		show = matches[0]
		season = int(matches[1])
		episode = int(matches[2])

		newName = '{0} - {1:0>2}x{2:0>2} - {3}{4}'.format(show, season, episode, metadata[season][episode], matches[3])
		
		result = raw_input('Moving {0} to {1}. Continue? (y/n)'.format(f, newName))
		if(result == 'y'):
			os.rename(orgFile, os.path.join(rootDir, newName))
		parsedFiles.append({'file': orgFile, 'newPath': os.path.join(rootDir, newName)})
	
	return parsedFiles