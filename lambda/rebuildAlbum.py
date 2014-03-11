import unirest

albumname = "santarita01"
key = "c2vwcOykEqC8DRjcHNsLkwIy3yNjUVrL"
albumkey = ''

response = unirest.get("https://lambda-face-recognition.p.mashape.com/album_rebuild?album=" + albumname + "&albumkey=" + albumkey,
  
  headers={
    "X-Mashape-Authorization": key
  }
)