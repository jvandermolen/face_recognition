import unirest, pickle

albumname = "santarita01"
key = "c2vwcOykEqC8DRjcHNsLkwIy3yNjUVrL"
albumkey = ''

pathsfile = 'fotos_por_nino_test_free.csv'
resultsfile = 'results.pkl'

print 'leyendo ' + albumname
with open(albumname, 'r') as f:
    for l in f.readlines():
        l = l.replace('\n', '')
        l = l.split(': ')
        if l[0] == 'albumkey':
            albumkey = l[1]

if albumkey == '':
    print 'Error al leer albumkey'
else:
    print 'albumkey obtenida'

results = []

print 'leyendo ' + pathsfile
with open(pathsfile, 'r') as f:
    for l in f.readlines():
        l = l.replace('\n', '')
        imgpath, personid = l.split(';')
        print 'testeando archivo: ' + imgpath

        response = unirest.post("https://lambda-face-recognition.p.mashape.com/recognize",
          
          headers={
            "X-Mashape-Authorization": key
          },
          params={ 
            "album": album,
            "albumkey": albumkey,
            "files": open(imgpath, mode="r"),
          }
        );
        response.body['actualid'] = personid
        print 'response body: ' + str(response.body)
        results.append(response)

print 'guardando resultados'
pickle.dump(results, open(resultsfile, 'wb'))