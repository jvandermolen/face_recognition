from looksAnalysis import *

#cargar archivos
la1 = looksAnalysis('la_v10_sininfo.pkl')
la2 = looksAnalysis('la_v10_coninfo.pkl')

#buscar en la1 bloques con interacciones que no estan en la2

blocks1 = set([(l.observer._id, str(l.date_time.date()), l.block or 'None') for l in la1.looks])
blocks2 = set([(l.observer._id, str(l.date_time.date()), l.block or 'None') for l in la2.looks])

difference = blocks1 - blocks2

filteredBlocks = set(['r1', 'r2', 'al'])

outfile = 'errors.csv'
with open(outfile, 'w') as o:
    l = ','.join(['id','fecha','bloque','inicio','fin']) + '\n'
    o.write(l)
    for d in difference:
        if d[2] in filteredBlocks: continue
        if d[2] == 'None':
            times = ['' , '']
        else:
            times = [str(t) for t in la1.getTimes(d[2])]
        d = list(d)
        d.extend(list(times))
        l = ','.join(d) + '\n'
        o.write(l)
