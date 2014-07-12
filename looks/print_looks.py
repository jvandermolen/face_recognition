from looksAnalysis import *
import sys

filename = sys.argv[1]

la = looksAnalysis(filename)

attr = ['interaction','observer._id','observer.names','observer.lastname1','observer.gender','date_time.strftime(\'%x\')', 'date_time.strftime(\'%X\')','date_time.isoweekday()','block','subject']
attr.extend(['observed._id','observed.names','observed.lastname1','observed.gender'])
headers = ['interaccion','id_alumno','nombres','apellido','genero','fecha','hora','dia','bloque','clase']
headers.extend(['id_observado','nombres_observado','apellido_observado','genero_observado'])
la.toCSV('miradas_' + filename[:-4] + '.csv','looks',attr,headers)
