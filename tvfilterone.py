import sys, io, os, re, shutil, string

#Returns files in the given directory that are larger than threshold bytes
def getFiles(dir, threshold):
    files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.getsize(os.path.join(dir, f)) > threshold]
    return files

def processMatches(fs, pattern):
    matches = [(f[0], pattern.search(f[1]), f[2]) for f in [(os.path.dirname(g), os.path.basename(g), g) for g in fs]]
    matches = [(f[0], f[1], f[2]) for f in matches if f[1]]
    repPattern = re.compile(r"[\._]|_UNPACK_")

    filtered = []
    for match in matches:
        filtered.append((match[2], formatName(match[1], repPattern), match[0]))
    return filtered

def formatName(match, repPat):
    groups = [string.capwords(repPat.sub(' ', f.strip().lower()).strip()) for f in match.groups() if f]
    print groups
    fString = os.path.join('{0}', 'Season {1:0>2}', '{0} - {1:0>2}x{2:0>2}')

    fString += '.avi'
    print fString.format(*groups)
    return fString.format(
            *groups)

def makeDirIfNecessary(filename):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)

def usage():
    print "Usage: tvfilterone.py directory threshold prefix"
    sys.exit()

if(len(sys.argv) != 4):
    usage()

files = getFiles(sys.argv[1], int(sys.argv[2]))
prefix = sys.argv[3]

print files

pattern1 = r"^([\w \.]*)[Ss]{1}(\d{1,2})[Ee]{1}(\d{1,2}).*$"
pattern2 = r"^([\w \.]*) ?-? ?(\d{1,2})[Xx]{1}(\d{1,2}).*$"
pattern3 = r"^([\w \.]*)(\d{1})(\d{2}).*$"

filtered = processMatches(files, re.compile(pattern1))
filtered.extend(processMatches(files, re.compile(pattern2)))
filtered.extend(processMatches(files, re.compile(pattern3)))
filtered = [(f[0], os.path.join(prefix, f[1])) for f in filtered]

for found in filtered:
    message = "creating directory at {2}, moving {0} to {1}. continue (y/n)".format(found[0], found[1], os.path.dirname(found[1]))
    result = raw_input(message)
    if(result == 'y'):
        makeDirIfNecessary(found[1])
        os.rename(found[0], found[1])
        #shutil.rmtree(os.path.dirname(found[0]))
