import unirest

albumname = "santarita_01"
key = "lzVlO8AVkc27FsBOYlBVI3yRcHlW6sHK"
albumkey = ''

pathsfile = 'fotos_train.csv'

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
        );

response = unirest.get("https://lambda-face-recognition.p.mashape.com/album_rebuild?album=" + album + "&albumkey=" + albumkey,
  
  headers={
    "X-Mashape-Authorization": key
  }
);