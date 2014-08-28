from looksAnalysis import *
import numpy as np
from datetime import datetime

la = looksAnalysis('save/la_ocv_v4.pkl')
path = '../faces/'
date_time = datetime.strptime('2012-11-27 11:27:00', '%Y-%m-%d %H:%M:%S')
observerId = '35'
observedId = '03'
la.showPhotos(path, date_time, observerId, observedId)
