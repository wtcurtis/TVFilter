import sys, io, os, re, shutil, string

def usage():
    print "usage: tvfilter.py directory prefix"
	sys.exit()

def getDirs(dirname):
    return [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]

def formatName(match, repPat):
    groups = [string.capwords(repPat.sub(' ', f.strip().lower()).strip()) for f in match.groups() if f]
    print groups
    fString = os.path.join('{0}', 'Season {1:0>2}', '{0} - {1:0>2}x{2:0>2}')

    fString += '.avi'

    return fString.format(
            *groups)

def processMatches(directory, pattern):
    matches = [(f, pattern.search(f)) for f in dirs]
    matches = [(f[0], f[1]) for f in matches if f[1]]
    repPattern = re.compile(r"[\._]|_UNPACK_")

    filtered = []
    for match in matches:
        filtered.append((os.path.join(dirname, match[0]), formatName(match[1], repPattern)))
    return filtered

def selector(a):
    return a[0]

def findFile(fi):
    files = os.listdir(fi)
    if len(files) > 0 :
        return max([(os.path.getsize(os.path.join(fi, f)), os.path.join(fi, f)) for f in os.listdir(fi)], key=selector)[1]
    else:
        return None

def makeDirIfNecessary(filename):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)

if len(sys.argv) != 3:
    usage()
    sys.exit()

leetGroups = ['HDTV','Xvid','ASAP','FQM','iNTERNAL','SUBS','PROPER']

dirname = sys.argv[1]
prefix = sys.argv[2]

dirs = getDirs(dirname)
files = [findFile(os.path.join(dirname, f)) for f in dirs]
print "Found {0} directories".format(len(dirs))

print files

pattern1 = r"^([\w \.]*)[Ss]{1}(\d{1,2})[Ee]{1}(\d{1,2}).*$"
pattern2 = r"^([\w \.]*) ?-? ?(\d{1,2})[Xx]{1}(\d{1,2}).*$"

filtered = processMatches(dirname, re.compile(pattern1))
filtered.extend(processMatches(dirname, re.compile(pattern2)))
filtered = [g for g in [(findFile(f[0]), os.path.join(prefix, f[1])) for f in filtered] if g[0]]

for found in filtered:
    message = "creating directory at {2}, moving {0} to {1}. continue (y/n)".format(found[0], found[1], os.path.dirname(found[1]))
    result = raw_input(message)
    if(result == 'y'):
        makeDirIfNecessary(found[1])
        os.rename(found[0], found[1])
        shutil.rmtree(os.path.dirname(found[0]))

#print "Matched on {0} directories".format(len(filtered))
