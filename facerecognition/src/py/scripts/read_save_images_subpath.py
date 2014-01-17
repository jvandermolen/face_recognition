import sys
# append tinyfacerec to module search path
sys.path.append("..")
# import numpy and matplotlib colormaps
import numpy as np
# import tinyfacerec modules
from tinyfacerec.util import read_images_subpath

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "USAGE: read_save_images_subpath.py </path/to/images> <label> </path/to/save>"
        sys.exit()
    
    # read images and save features and labels
    [X,y] = read_images_subpath(sys.argv[1], int(sys.argv[2]), sys.argv[3], sz=[92, 112])
