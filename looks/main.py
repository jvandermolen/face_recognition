from looksAnalysis import *
import sys

filename = sys.argv[1]

la = looksAnalysis()

la.setTimetable('horario2.csv', 'bloques2.csv')
la.setPeople('personas.csv')
la.setVideos('duracion_videos_completo.csv')
la.setLooks('matrices.csv', delta=60, useVideos=False)

la.save(filename)

print len(la.looks)
