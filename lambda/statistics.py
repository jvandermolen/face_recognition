import pickle
import numpy as np

albumname = "santarita01"
resultsfile = 'results_' + albumname + '.pkl'

results = pickle.load(open(resultsfile, 'rb'))

actual = range(len(results))
predicted = range(len(results))
for i in xrange(len(results)):
    r = results[i]
    actual[i] = r.body['actualid']
    try:
        predicted[i] = r.body['photos'][0]['tags'][0]['uids'][0]['predicted']
    except:
        predicted[i] = '-1'

accuracy =  np.mean( actual == predicted )*100

print 'acierto en la prediccion: ' + str(accuracy) + '%'