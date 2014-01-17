listfile = 'todaslasmatrices.txt'
#abrir lista de archivos
with open(listfile, 'r') as fl:
#por cada archivo
    for filename in fl.readlines():
#abrir el archivo
        with open(filename.replace('\n', ''), 'r') as f:
#cada linea corresponde a un archivo de salida
            for line in f.readlines():
#sacar el salto de linea
                line = line.replace('\n', '')
#sacar el tosparse()
                line = line.replace('tosparse(', '')
                line = line.replace(');', '')
#reemplazar el nombre del arreglo por A
                equals = line.index('=')
                name = line[:equals]
                line = line.replace(name, 'A ')
#escribir en el archivo de salida
                outfile = name.replace('d', '') + '.txt'
                with open(outfile, 'w') as o:
                    o.write(line)
