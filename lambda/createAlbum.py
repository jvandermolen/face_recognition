import unirest

albumname = "santarita_01"
key = "lzVlO8AVkc27FsBOYlBVI3yRcHlW6sHK"

response = unirest.post("https://lambda-face-recognition.p.mashape.com/album",
  
  headers={
    "X-Mashape-Authorization": key
  },
  params={ 
    "album": albumname
  }
);
print response.body
with open(albumname, 'w') as f:
    f.write('album: ' + response.body['album'] + '\n')
    f.write('album key: ' + response.body['albumkey'])
print albumname + 'creado'
