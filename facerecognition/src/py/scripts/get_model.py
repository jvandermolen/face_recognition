import sys, os, pickle
# append tinyfacerec to module search path
sys.path.append("..")
# import numpy and matplotlib colormaps
import numpy as np
# import tinyfacerec modules
from tinyfacerec.model import FisherfacesModel

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "USAGE: get_model.py </path/to/data> <rate_data_to_train> </path/to/save>"
        sys.exit()
    
    # read data
    X, y = [], []
    pathToData = sys.argv[1]
    trainRate = float(sys.argv[2])
    pathToSave = sys.argv[3]
    for filename in os.listdir(pathToData):
        try:
            npzfile = np.load(os.path.join(pathToData, filename))
            auxX = list(npzfile['X'])
            auxy = list(npzfile['y'])
            nTrain = int(len(auxy)*trainRate)
            X.extend(auxX[:nTrain])
            y.extend(auxy[:nTrain])
        except IOError as e:
            print filename + ' - ' + "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
    # compute the eigenfaces model
    print "computing model with " + str(len(X)) + " photos"
    model = FisherfacesModel(X, y)
    # save the model
    print "saving model"
    outfile = os.path.basename(os.path.normpath(pathToData)).replace('data', 'model') + '_' + str(trainRate) + '.pkl'
    outpath = os.path.join(pathToSave, outfile)
    outpkl = open(outpath, 'wb')
    pickle.dump(model, outpkl, -1)
    outpkl.close()
