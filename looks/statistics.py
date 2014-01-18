from looksAnalysis import *
import sys
import numpy as np
import scipy.stats as stats

filename = sys.argv[1]

la = looksAnalysis(filename)

def per(f,n):
    return float(f)/float(n)*100

def print_result(title, res, decimals=1, tex=None, write=True):
    nCols = len(res[0])
    print
    print title
    colLen = [0 for i in range(nCols)]
    for row in res:
        colLen = [max(cL, len(str(r))) for cL, r in zip(colLen,row)]
    print '-'*(np.sum(colLen) + 3*len(row) + 1)
    for row in res:
        print '| ' + ' | '.join([('{'+str(n)+':' + str(colLen[n]) + '.' + str(decimals) + 'f}') if isinstance(row[n], float) else ('{'+str(n)+':' + str(colLen[n]) + '}') for n in range(len(row))]).format(*row) + ' |'
    print '-'*(np.sum(colLen) + 3*len(row) + 1)

    #tex
    t = ''
    if not tex is None:
        if nCols < 2:
            t = '\\begin{table}[h!]\n\\begin{center}\n\\begin{tabular}{|c|}\n\\hline\n'
        else:
            t = '\\begin{table}[h!]\n\\begin{center}\n\\begin{tabular}{|l|' + '|'.join(['r' for i in range(nCols-1)]) + '|}\n\\hline\n'
        for row in res:
            t += ' & '.join([('{'+str(n)+':' + str(colLen[n]) + '.' + str(decimals) + 'f}') if isinstance(row[n], float) else ('{'+str(n)+':' + str(colLen[n]) + '}') for n in range(len(row))]).format(*row) + '\\\\ \\hline\n'

        t += '\\end{tabular}\n\\caption{' + title + '}\n\\end{center}\n\\end{table}\n\n'
        t = t.replace('_', '\\_').replace('<=', '$\leq$').replace('>', '$>$')
        if write:
            tex.write(t)
    return t, nCols

def print_ttest(title, sample1, sample2, header, values, tex=None):
    means = [np.mean(sample1), np.mean(sample2)]
    freqs = [len(sample1), len(sample2)]
    sems = [np.std(sample1)/np.sqrt(freqs[0]), np.std(sample2)/np.sqrt(freqs[1])]
    statistic, pvalue = stats.ttest_ind(sample1, sample2)
    matrix = [[header, 'tiempo de grabacion', 'media', 'error. est.']]
    matrix.extend([[v, n, m, s] for v, n, m, s in zip(values, freqs, means, sems)])
    t, nCols = print_result(title, matrix, decimals=3 , tex=tex, write=False)
    l = 'p-valor: %2.3f' %pvalue
    print l
    
    #tex
    if not tex is None:
        t = t.replace('\\end{tabular}', '\\multicolumn{' + str(nCols) + '}{|c|}{' + l + '} \\\\ \\hline\n\\end{tabular}')
        tex.write(t)

la.looks = [l for l in la.looks if l.block in ['1_2', '3_4', '5_6', '7_8']]

tex = open('./tex/statistics.tex', 'w')

pre = '\\documentclass[spanish]{article}\n\\usepackage[spanish, activeacute]{babel}\n\\usepackage[latin1]{inputenc}\n\\usepackage{amssymb}\n\\usepackage{amsmath,latexsym,amsthm}\n\\usepackage{graphicx}\n\n\\begin{document}\n'
tex.write(pre)

###########################################################
#frecuencias
###########################################################
print 'FRECUENCIAS'

#total obs
n = len(la.looks)

print_result('total de observaciones', [['n'], [n]], tex=tex)

#porcentaje de ceros y unos
n0 = len([l for l in la.looks if l.interaction == 0])
p0 = per(n0,n)
n1 = len([l for l in la.looks if l.interaction == 1])
p1 = per(n1,n)

print_result('frecuencia de interacciones', [['Interaccion', 'frecuencia' , 'porcentaje'], ['no', n0, p0], ['si', n1, p1]], tex=tex)

#porcentaje segun rol
n0 = len([l for l in la.looks if int(l.observer._id) == 0])
p0 = per(n0,n)
n1 = len([l for l in la.looks if int(l.observer._id) != 0 and l.observer.gender == '1'])
p1 = per(n1,n)
n2 = len([l for l in la.looks if int(l.observer._id) != 0 and l.observer.gender == '2'])
p2 = per(n2,n)

print_result('tiempo estudiado segun rol y sexo', [['rol y sexo', 'tiempo (minutos)' , 'porcentaje'], ['profesor', n0, p0], ['alumna', n2, p2], ['alumno', n1, p1]], tex=tex)

#tiempo estudiado segun hora del dia
n1 = len([l for l in la.looks if l.block == '1_2'])
p1 = per(n1,n)
n2 = len([l for l in la.looks if l.block == '3_4'])
p2 = per(n2,n)
n3 = len([l for l in la.looks if l.block == '5_6'])
p3 = per(n3,n)
n4 = len([l for l in la.looks if l.block == '7_8'])
p4 = per(n4,n)

print_result('tiempo estudiado segun hora del dia', [['modulo', 'tiempo (minutos)' , 'porcentaje'], ['1_2', n1, p1], ['3_4', n2, p2], ['5_6', n3, p3], ['7_8', n4, p4]], tex=tex)

#tiempo estudiado segun dia de la semana
n1 = len([l for l in la.looks if l.date_time.isoweekday() == 1])
p1 = per(n1,n)
n2 = len([l for l in la.looks if l.date_time.isoweekday() == 2])
p2 = per(n2,n)
n3 = len([l for l in la.looks if l.date_time.isoweekday() == 3])
p3 = per(n3,n)
n4 = len([l for l in la.looks if l.date_time.isoweekday() == 4])
p4 = per(n4,n)
n5 = len([l for l in la.looks if l.date_time.isoweekday() == 5])
p5 = per(n5,n)

print_result('tiempo estudiado segun dia de la semana', [['dia', 'tiempo (minutos)' , 'porcentaje'], ['Lunes', n1, p1], ['Martes', n2, p2], ['Miercoles', n3, p3], ['Jueves', n4, p4], ['Viernes', n5, p5]], tex=tex)

#tiempo estudiado segun asignatura
values = ['Arte', 'Ciencias', 'Ed_fisica', 'Historia', 'Integra', 'Lenguaje', 'Mate_Labo', 'Matematica', 'Religion', 'Tecnologica', '']
fs = [len([l for l in la.looks if l.subject == v]) for v in values]
ps = [per(f,n) for f in fs]
title = 'tiempo estudiado segun asignatura'
matrix = [['asignatura', 'tiempo (minutos)', 'porcentaje']]
matrix.extend([[v, f, p] for v, f, p in zip(values, fs, ps)])
print_result(title, matrix, tex=tex)

#minutos de uso de los lentes por sujeto
values = range(37)
fs = [len([l for l in la.looks if int(l.observer._id) == v]) for v in values]
ps = [per(f,n) for f in fs]
title = 'minutos de uso de los lentes por sujeto'
matrix = [['sujeto', 'tiempo (minutos)', 'porcentaje']]
matrix.extend([[v, f, p] for v, f, p in zip(values, fs, ps)])
print_result(title, matrix, tex=tex)

###########################################################
#comparacion de medias
###########################################################
print 'COMPARACION DE MEDIAS'

#promedio segun rol
teacher = [l.interaction for l in la.looks if int(l.observer._id) == 0]
students = [l.interaction for l in la.looks if int(l.observer._id) != 0]
print_ttest('promedio segun rol', students, teacher, 'rol', ['alumnos','profesor'], tex=tex)

#alumnos segun sexo
males = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 1]
females = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 2]
print_ttest('promedio segun sexo del alumno', females, males, 'sexo', ['femenino','masculino'], tex=tex)

#promedio segun enfoque de asignatura
sub1 = ('Arte', 'Tecnologica', 'Religion')
sub2 = ('Matematica', 'Lenguaje', 'Ciencias', 'Historia')
first = [l.interaction for l in la.looks if int(l.observer._id) != 0 and l.subject in sub1]
second = [l.interaction for l in la.looks if int(l.observer._id) != 0 and l.subject in sub2]
print_ttest('alumnos: promedio segun enfonque de la asignatura', first, second, 'grupo', ['primero','segundo'], tex=tex)

first = [l.interaction for l in la.looks if int(l.observer._id) == 0 and l.subject in sub1]
second = [l.interaction for l in la.looks if int(l.observer._id) == 0 and l.subject in sub2]
print_ttest('profesor: promedio segun enfonque de la asignatura', first, second, 'grupo', ['primero','segundo'], tex=tex)

#promedio segun horario
bl1 = ('1_2', '3_4')
bl2 = ('5_6', '7_8')
first = [l.interaction for l in la.looks if int(l.observer._id) != 0 and l.block in bl1]
second = [l.interaction for l in la.looks if int(l.observer._id) != 0 and l.block in bl2]
print_ttest('alumnos: promedio segun bloque horario', first, second, 'grupo', ['1_2 y 3_4', '5_6 y 7_8'], tex=tex)

first = [l.interaction for l in la.looks if int(l.observer._id) == 0 and l.block in bl1]
second = [l.interaction for l in la.looks if int(l.observer._id) == 0 and l.block in bl2]
print_ttest('profesor: promedio segun bloque horario', first, second, 'grupo', ['1_2 y 3_4', '5_6 y 7_8'], tex=tex)

#promedio segun rendimiento academico
grades = [o.getMean('grades') for o in la.people if int(o._id) != 0]

mean = np.mean(grades)
obsBelow = [i+1 for i in range(len(grades)) if grades[i] <= mean]
obsAbove = [i+1 for i in range(len(grades)) if grades[i] > mean]
below = [l.interaction for l in la.looks if int(l.observer._id) in obsBelow]
above = [l.interaction for l in la.looks if int(l.observer._id) in obsAbove]
print_ttest('alumnos bajo el promedio de notas versus sobre promedio de notas', below, above, 'promedio de notas', ['<= 5.17', '> 5.17'], tex=tex)

score1 = stats.scoreatpercentile(grades, 33)
score2 = stats.scoreatpercentile(grades, 67)
obsBelow = [i+1 for i in range(len(grades)) if grades[i] <= score1]
obsAbove = [i+1 for i in range(len(grades)) if grades[i] > score2]
below = [l.interaction for l in la.looks if int(l.observer._id) in obsBelow]
above = [l.interaction for l in la.looks if int(l.observer._id) in obsAbove]
print_ttest('alumnos tercio con peores notas versus tercio con mejores notas', below, above, 'promedio de notas', ['Bajo', 'Alto'], tex=tex)

#promedio segun evaluacion de companeros
evs = [o.getMean('evaluation') for o in la.people if int(o._id) != 0]

mean = np.mean([e for e in evs if not (e is None or np.isnan(e))])
obsBelow = [i+1 for i in range(len(evs)) if evs[i] <= mean]
obsAbove = [i+1 for i in range(len(evs)) if evs[i] > mean]
below = [l.interaction for l in la.looks if int(l.observer._id) in obsBelow]
above = [l.interaction for l in la.looks if int(l.observer._id) in obsAbove]
print_ttest('alumnos bajo el promedio de evaluacion versus sobre promedio de evaluacion', below, above, 'prom. de evaluacion', ['<= 4.52', '> 4.52'], tex=tex)

score1 = stats.scoreatpercentile(evs, 33)
score2 = stats.scoreatpercentile(evs, 67)
obsBelow = [i+1 for i in range(len(evs)) if evs[i] <= score1]
obsAbove = [i+1 for i in range(len(evs)) if evs[i] > score2]
below = [l.interaction for l in la.looks if int(l.observer._id) in obsBelow]
above = [l.interaction for l in la.looks if int(l.observer._id) in obsAbove]
print_ttest('alumnos tercio con peores evaluaciones versus tercio con mejores evaluaciones', below, above, 'prom. de evaluacion', ['Bajo', 'Alto'], tex=tex)

#interacciones en asignaturas segun sexo
femaleMath = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 2 and l.subject == 'Matematica']
maleMath = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 1 and l.subject == 'Matematica']
print_ttest('interacciones segun sexo en matematicas', femaleMath, maleMath, 'sexo', ['Femenino', 'Masculino'], tex=tex)

femaleLang = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 2 and l.subject == 'Lenguaje']
maleLang = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 1 and l.subject == 'Lenguaje']
print_ttest('interacciones segun sexo en lenguage', femaleLang, maleLang, 'sexo', ['Femenino', 'Masculino'], tex=tex)

femaleArts = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 2 and l.subject == 'Arte']
maleArts = [l.interaction for l in la.looks if int(l.observer._id) != 0 and int(l.observer.gender) == 1 and l.subject == 'Arte']
print_ttest('interacciones segun sexo en artes', femaleArts, maleArts, 'sexo', ['Femenino', 'Masculino'], tex=tex)

#interacciones en matematicas segun nivel en matematicas
mathGrades = [o.grades[5] for o in la.people if int(o._id) != 0]

score1 = stats.scoreatpercentile(mathGrades, 33)
score2 = stats.scoreatpercentile(mathGrades, 67)
obsBelow = [i+1 for i in range(len(mathGrades)) if mathGrades[i] <= score1]
obsAbove = [i+1 for i in range(len(mathGrades)) if mathGrades[i] > score2]
below = [l.interaction for l in la.looks if int(l.observer._id) in obsBelow and l.subject == 'Matematica']
above = [l.interaction for l in la.looks if int(l.observer._id) in obsAbove and l.subject == 'Matematica']
print_ttest('interacciones segun promedio de matematicas en matematicas', below, above, 'promedio de notas', ['Bajo', 'Alto'], tex=tex)

#promedio de interacciones por sujeto
values = range(37)
ss = [[l.interaction for l in la.looks if int(l.observer._id) == v] for v in values]
fs = [len(s) for s in ss]
ms = [np.mean(s)*100 for s in ss]
title = 'promedio de interacciones por sujeto'
matrix = [['sujeto', 'tiempo (minutos)', 'promedio de interacciones']]
matrix.extend([[v, f, m] for v, f, m in zip(values, fs, ms)])
print_result(title, matrix, tex=tex)

tex.write('\n\\end{document}')
tex.close()

#PONER ERROR TIPICO DE LA MEDIA Y NO DESVIACION DE LA VARIABLE EN T-TESTS
#REVISAR TIEMPOS DE VIDEOS Y COMPARAR CON TABLA DE RAGNAR
#VER LO DE PICASSA
#ECUALIZAR