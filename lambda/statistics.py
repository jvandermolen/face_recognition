import pickle
import numpy as np

albumname = "santarita01"
resultsfile = 'results_' + albumname + '.pkl'

results = pickle.load(open(resultsfile, 'rb'))

for r in results:
    if not 'photos' in r.body.keys():
        r.body['photos'] = [{'tags':[{'uids':[{'predicted':'no recognition'}]}]}]

ids = [ ( r.body['actualid'], [r.body['photos'][0]['tags'][0]['uids'][0]['predicted'] ) for r in results ]
actual, predicted = zip(*ids)
accuracy =  np.mean( actual == predicted )*100

print 'acierto en la prediccion: ' + str(accuracy) + '%'