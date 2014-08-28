from looksAnalysis import *
import numpy as np
from datetime import datetime

la = looksAnalysis('save/la_ocv_v4.pkl')
date_time0 = datetime(2012,9,26,)
O = [v.observer for v in la.videos if v.date_time <= date_time0 < v.getEnd()]