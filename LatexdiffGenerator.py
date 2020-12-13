import sys,os,shutil,traceback
from pathlib import Path

def isGenerated(file):
    ignoredFileEndings = [".tex",".aux",".lof",".log",".lot",".fls",".out",
    ".toc",".fmt",".fot",".cb",".cb2",".lb",".dvi",".xdv","-converted-to.",
    ".pdf",".bbl",".bcf",".blg","-blx.aux","-blx.bib",".run.xml",".synctex",".pdfsync"]

    for e in ignoredFileEndings:
        if e in file:
            return True
    return False

def removePathFromString(toRemove, pathArray):
    newPaths = []
    for p in pathArray:
        newP = str(p).replace(toRemove,"")
        newPaths.append(newP)
    
    return newPaths

def getFilesInPath(path,pattern,wantString):
    #return list(Path(".").rglob("*.[tT][xX][tT]"))
    posixPaths = list(Path(path).rglob(pattern))
    if wantString:
        pathStrings = []
        for p in posixPaths:
            pathStrings.append(str(p.resolve()))
        return pathStrings
    else:
        return posixPaths
    
def getPathsFromArgs():
    return sys.argv[1:]

def extendToFullPath(path):
    os.chdir(path)
    newPath = os.getcwd()
    os.chdir("..")
    return newPath

def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# Default Values
newDir = "latexdiff-doc"

# Check args
paths = getPathsFromArgs()
if len(paths) < 2 or len(paths) >= 4:
    print("Not enough (at least 2) or too many (more than 3) arguments")
    sys.exit()
elif paths[0] == "" or paths[1] == "":
    print("source paths cannot be empty")
    sys.exit()
elif len(paths) == 3:
    newDir = paths[2]

# Extend paths
paths[0] = extendToFullPath(paths[0])
paths[1] = extendToFullPath(paths[1])

# Get directory names
firstDirSplitList = paths[0].split("/")
firstDir = firstDirSplitList[len(firstDirSplitList)-1]
secondDirSplitList = paths[1].split("/")
secondDir = secondDirSplitList[len(secondDirSplitList)-1]

# Get directory structures
doc1 = getFilesInPath(paths[0],"*.tex",True)
cleanDocs = removePathFromString(paths[0],doc1)
structure = fast_scandir(paths[0])
structureRelative = []

for s in structure:
    structureRelative.append(str(s.replace(paths[0],"")))
if os.path.isdir(newDir):
    shutil.rmtree(newDir)

# Make new directory with subdirectories
os.mkdir(newDir)
for reldir in structureRelative:
    os.mkdir(newDir+reldir)

# Get tree of files to copy and remove generated and tex files and copy files
copyTree = getFilesInPath(paths[0],"*",False)
copyTree[:] = [item for item in copyTree if not isGenerated(str(item))]
copyTree = removePathFromString(paths[0],copyTree)

for c in copyTree:
    try:
        shutil.copy(firstDir+str(c),newDir+str(c))
    except:
        traceback.print_exc()

# Generate Latexdiff project
i = 0
while i < len(cleanDocs):
    first = "./"+firstDir+cleanDocs[i]
    second = "./"+secondDir+cleanDocs[i]
    dest = "./"+newDir+cleanDocs[i]
    cmd = "latexdiff "+first +" "+second + " > " + dest
    print(cmd)
    os.system(cmd) 
    i += 1