from looksAnalysis import *
from datetime import datetime

folder = 'matrices/'

la = looksAnalysis('save/la_ocv_v4.pkl')

t0 = '080000'
t1 = '160000'
days = ['20120926','20121001','20121002','20121003','20121004','20121005','20121008','20121009','20121011','20121016','20121019','20121022']
days.extend(['20121024','20121026','20121029','20121106','20121108','20121119','20121120','20121123','20121126','20121127'])

#for day in days:
#    date_time0 = datetime.strptime(day+t0, '%Y%m%d%H%M%S')
#    date_time1 = datetime.strptime(day+t1, '%Y%m%d%H%M%S')
#    la.printMatrix(date_time0, date_time1, folder)
la.printMatrix(datetime.strptime(days[0]+t0, '%Y%m%d%H%M%S'), datetime.strptime(days[-1]+t1, '%Y%m%d%H%M%S'), ('subject', ['Matematica']), 'gender')