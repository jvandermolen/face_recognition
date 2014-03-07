import unirest

albumname = "santarita01"
key = "c2vwcOykEqC8DRjcHNsLkwIy3yNjUVrL"

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

response = unirest.get("https://lambda-face-recognition.p.mashape.com/album?album=" + albumname + "&albumkey=" + albumkey,
  
  headers={
    "X-Mashape-Authorization": key
  }
)

print 'response body: ' + str(response.body)