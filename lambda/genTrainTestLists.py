from collections import Counter
import random

def readPhotosCsv( filename, delimeter=';' ):
    with open(filename, 'r') as f:
        linePairs = f.readlines()
        linePairs = [tuple(l[:-1].split( delimeter )) for l in linePairs]
    return linePairs

def writePhotosCsv( filename, lines, delimeter=';'):
    with open(filename, 'w') as f:
        s = '\n'.join( [ delimeter.join(l) for l in lines ] )
        f.write(s)

def diff(a, b):
        b = set(b)
        return [aa for aa in a if aa not in b]

photosFile = '../facerecognition/fotos_por_nino.csv'
trainFile = photosFile.replace('.csv', '_train.csv')
testFile = photosFile.replace('.csv', '_test.csv')

trainRate = 0.5

paths, ids = zip( *readPhotosCsv( photosFile ) )
print 'rutas de fotos e ids obtenidos'
counts = Counter(ids)
print 'total de fotos por id obtenidos'

trLines = []
teLines = []

for key in sorted(counts.keys()):
    print 'analizando id: ' + key
    inds = [i for i in range(len(ids)) if ids[i]==key]
    trInds = sorted( random.sample( inds, int( trainRate * counts[key] ) ) )
    teInds = diff(inds, trInds)
    trLines.extend( [ ( paths[i], ids[i] ) for i in trInds ] )
    teLines.extend( [ ( paths[i], ids[i] ) for i in teInds ] )

writePhotosCsv( trainFile, trLines )
print 'archivo creado: ' + trainFile
writePhotosCsv( testFile, teLines )
print 'archivo creado: ' + testFile