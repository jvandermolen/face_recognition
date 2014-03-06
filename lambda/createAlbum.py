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

with open(albumname, 'w') as f:
    f.write('album: ' + response['album'] + '\n')
    f.write('album key: ' + response['albumkey'])
print albumname + 'creado'