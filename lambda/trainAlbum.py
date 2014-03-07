import unirest

albumname = "santarita_01"
key = "c2vwcOykEqC8DRjcHNsLkwIy3yNjUVrL"
albumkey = ''

pathsfile = 'fotos_por_nino_train.csv'

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

print 'leyendo ' + pathsfile
with open(pathsfile, 'r') as f:
    for l in f.readlines():
        l = l.replace('\n', '')
        imgpath, personid = l.split(';')
        print 'agregando archivo: ' + imgpath

        response = unirest.post("https://lambda-face-recognition.p.mashape.com/album_train",
  
          headers={
            "X-Mashape-Authorization": key
          },
          params={ 
            "album": albumname,
            "albumkey": albumkey,
            "entryid": personid,
            "files": open(imgpath, mode="r"),
          }
        )
        print 'response body: ' + str(response.body)

response = unirest.get("https://lambda-face-recognition.p.mashape.com/album_rebuild?album=" + album + "&albumkey=" + albumkey,
  
  headers={
    "X-Mashape-Authorization": key
  }
)