import sys, io, os, re, shutil, string

#Returns files in the given directory that are larger than threshold bytes
def getFiles(dir, threshold):
    files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.getsize(os.path.join(dir, f)) > threshold]
    return files

def getDirs(dirname):
    return [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]

def formatName(match, repPat):
    groups = [string.capwords(repPat.sub(' ', f.strip().lower()).strip()) for f in match.groups() if f]
    fString = os.path.join('{0}', 'Season {1:0>2}', '{0} - {1:0>2}x{2:0>2}')

    fString += '.avi'

    return fString.format(*groups)

def makeDirIfNecessary(filename):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)


#Get multiple file matches from a single directory
def getMatchesSingle(fs, pattern):
    matches = [(f[0], pattern.search(f[1]), f[2]) for f in [(os.path.dirname(g), os.path.basename(g), g) for g in fs]]
    matches = [(f[0], f[1], f[2]) for f in matches if f[1]]
    repPattern = re.compile(r"[\._]|_UNPACK_")

    filtered = []
    for match in matches:
        filtered.append((match[2], formatName(match[1], repPattern), match[0]))
    return filtered

def getMatchesMulti(directory, pattern):
    dirs = getDirs(directory)
    matches = [(f, pattern.search(f)) for f in dirs]
    matches = [(f[0], f[1]) for f in matches if f[1]]
    repPattern = re.compile(r"[\._]|_UNPACK_")

    filtered = []
    for match in matches:
        filtered.append((os.path.join(directory, match[0]), formatName(match[1], repPattern)))
    return filtered

def moveAll(filtered):
    moved = []
    for found in filtered:
        message = "creating directory at {2}, moving {0} to {1}. continue (y/n)".format(found[0], found[1], os.path.dirname(found[1]))
        result = raw_input(message)
        if(result == 'y'):
            makeDirIfNecessary(found[1])
            os.rename(found[0], found[1])
            moved.append(found)

    return moved

def findFile(fi):
    files = os.listdir(fi)
    if len(files) > 0 :
        return max([(os.path.getsize(os.path.join(fi, f)), os.path.join(fi, f)) for f in os.listdir(fi)], key=selector)[1]
    else:
        return None

def selector(a):
    return a[0]

def usage():
    print "Usage: tvfilterone.py directory threshold prefix"
    sys.exit()

def processMulti(dirname, prefix, patterns = [r"^([\w \.]*)[Ss]{1}(\d{1,2})[Ee]{1}(\d{1,2}).*$",
                                              r"^([\w \.]*) ?-? ?(\d{1,2})[Xx]{1}(\d{1,2}).*$"]):
    #dirs = getDirs(dirname)
    #files = [findFile(os.path.join(dirname, f) for f in dirs)]

    filtered = []
    compiledPatterns = [re.compile(a) for a in patterns]
    for pattern in compiledPatterns:
        filtered.extend(getMatchesMulti(dirname, pattern))
    filtered = [g for g in [(findFile(f[0]), os.path.join(prefix, f[1])) for f in filtered] if g[0]]

    return moveAll(filtered)



def processSingle(directory, threshold, prefix, patterns = [r"^([\w \.]*)[Ss]{1}(\d{1,2})[Ee]{1}(\d{1,2}).*$",
                                                      r"^([\w \.]*) ?-? ?(\d{1,2})[Xx]{1}(\d{1,2}).*$",
                                                      r"^([\w \.]*)(\d{1})(\d{2}).*$"]):
    files = getFiles(directory, threshold)
    print files

    compiledPatterns = [re.compile(a) for a in patterns]
    filtered = []
    for pattern in compiledPatterns:
        filtered.extend(getMatchesSingle(files, pattern))

    filtered = [(a[0], os.path.join(prefix, a[1])) for f in filtered]

    return moveAll(filtered)
