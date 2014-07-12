from looksAnalysis import *
import numpy as np

#la = looksAnalysis('la_convideos.pkl')
#ms=la.matlab2numpy('./matrices_avelio/1123.txt', True)
#i=-1
#for m in ms:
#    i += 1
#    if len(m.keys())==0: continue
#    print i
#    print m

#print len(la.videos)
#for v in la.videos:
#    if v.observer._id == '0' and v.date_time.isoweekday() == 5:
#        print v.observer._id + ' - ' + str(v.date_time)

#la = looksAnalysis()
#m = la.matlab2numpy('./matrices/1019.txt', True)
#print m[242]

la = looksAnalysis('save/la_ocv_v3.pkl')
print la.looks[60].observer._id