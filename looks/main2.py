from looksAnalysis import *
import sys
from datetime import datetime

filename = sys.argv[1]

la = looksAnalysis()

la.setTimetable('horario2.csv', 'bloques2.csv')
la.setPeople('personas.csv')
la.setVideos('duracion_videos_completo.csv')
la.setExactLooks('faces_folders2.txt', 30)

t0 = '080000'
t1 = '160000'
days = ['20120926','20121001','20121002','20121003','20121004','20121005','20121008','20121009','20121011','20121016','20121019','20121022']
days.extend(['20121024','20121025','20121026','20121029','20121106','20121108','20121119','20121120','20121123','20121126'])
datetimeList = []
for day in days:
    datetimeList.append((datetime.strptime(day+t0, '%Y%m%d%H%M%S'), datetime.strptime(day+t1, '%Y%m%d%H%M%S')))
la.setLooks2(datetimeList, 60, useVideos=False)

la.save(filename)

print len(la.looks)
