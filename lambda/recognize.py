import unirest, pickle

albumname = "santarita_01"
key = "lzVlO8AVkc27FsBOYlBVI3yRcHlW6sHK"
albumkey = ''

pathsfile = 'fotos_test.csv'
resultsfile = 'results.pkl'

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

        response['actualid'] = personid
        results.append(response)

print 'guardando resultados'
pickle.dump(results, open(resultsfile, 'wb'))