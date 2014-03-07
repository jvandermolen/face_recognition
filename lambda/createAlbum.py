import unirest

albumname = "santarita_01"
key = "c2vwcOykEqC8DRjcHNsLkwIy3yNjUVrL"

response = unirest.post("https://lambda-face-recognition.p.mashape.com/album",
  
  headers={
    "X-Mashape-Authorization": key
  },
  params={ 
    "album": albumname
  }
)
print 'response body: ' + str(response.body)
with open(albumname, 'w') as f:
    f.write('album: ' + response.body['album'] + '\n')
    f.write('album key: ' + response.body['albumkey'])
print albumname + 'creado'
