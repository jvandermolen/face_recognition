newId = {}

filename = 'resources/conversion_lista_alumnos.csv'
with open(filename, 'r') as f:
    for row in f:
        row = row.replace('\n','').split(',')
        newId[row[0]] = row[1]
newId['todos'] = 'todos'
newId[''] = ''

infile = 'resources/inasistencias.csv'
outfile = 'resources/inasistencias2.csv'
with open(infile, 'r') as inf:
    with open(outfile, 'w') as outf:
        blocks = inf.readline()
        outf.write(blocks)
        for row in inf:
            row = row.replace('\n','').split(',')
            print 'analizando fila: ' + str(row)
            day = row[0]
            line = [day]
            for i in range(len(row[1:])):
                el = '-'.join([newId[ ln ] for ln in row[i+1].split('-')])
                line.append(el)
            line = ','.join(line) + '\n'
            outf.write(line)