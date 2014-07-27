from datetime import datetime, timedelta, time
from looksAnalysis import video, clip

filename = 'videos_length.txt'
outfile = 'videos_data.csv'

def videofoldername2data(folder):
    #ejemplo: 20120926_01_08_Dilan
    fields = folder.split('_')
    observerId = fields[2]
    return observerId

def videofilename2data(filename):
    #ejemplo: 1_a_20120926082315_Dilan.AVI
    fields = filename.replace('.jpg','').split('_')
    block = fields[0]
    clipId = fields[1]
    date_time = datetime.strptime(fields[2], '%Y%m%d%H%M%S')
    return block, clipId, date_time

def getVideo(videoId, videos):
    ids = [i for i in range(len(videos)) if videos[i]._id == videoId]
    return ids

def getClipDuration(v, clipId):
    try:
        d = v.getClip(clipId).duration
    except:
        d = '0'
    return d


bloque = {'1':'1_2', '3':'3_4', '5':'5_6', '7':'7_8'}
dia = ['LU','MA','MI','JU','VI','SA','DO']
nombre = ['Profesor', 'Claudia', 'Barbara', 'Ignacio', 'Sebastian', 'Eduardo', 'Jordan', 'Alexis', 'Dilan', 'Maria Jose', 'Susana', 
    'Nayareth', 'Catalina', 'Francisco', 'Benjamin', 'Matias', 'Dania', 'Brithanny', 'Ignacio', 'Constanza', 'Joseph', 
    'David', 'Jorky', 'Jane', 'Noemi', 'Belen', 'Bryan', 'Scarlet', 'Lee', 'Victor', 'Jeremy', 'Patricio', 'Nicolas', 
    'Maria', 'Oscar', 'Felipe', 'Cristofer']

apellido = ['Stenio', 'Antilical', 'Arriagada', 'Arteaga', 'Avendano', 'Cabezas', 'Carvajal', 'Catrilaf', 'Fuentes', 'Garces', 'Gomez', 
    'Gonzalez', 'Gonzalez', 'Huerta', 'Huerta', 'Huircaman', 'Hurtado', 'Inalaf', 'Jara', 'Jara', 'Lira', 
    'Madariaga', 'Mancilla', 'Marquez', 'Maturana', 'Norambuena', 'Palma', 'Parada', 'Perez', 'Poblete', 'Poza', 'Rivera', 'Roa', 
    'Sandoval', 'Valencia', 'Yevenes', 'Zuniga']

genero = ['M', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'F', 'F', 'M', 'F', 'M', 
    'M', 'F', 'F', 'F', 'F', 'M', 'F', 'F', 'M', 'M', 'M', 'M', 'F', 'M', 'M', 'M']

videos = []

with open(filename, 'r') as f:
    for row in f.readlines():
        row = row.split(' - ')
        videoPath = row[0]
        length = row[1][:-1]
        pathParts = videoPath.split('/')
        folder = pathParts[-2]
        name = pathParts[-1]

        observerId = videofoldername2data(folder)
        block, clipId, date_time = videofilename2data(name)

        videoId = '-'.join([ date_time.strftime('%Y%m%d'), block, observerId ])
        clp = clip(clipId, length)

        ids = getVideo(videoId, videos)
        if len(ids) == 0:
            clips = [clp]
            v = video(videoId, date_time, bloque[block], None, observerId, None, clips, None)
            videos.append(v)
        elif len(ids) > 1:
            print 'error: video ' + videoId + ' duplicado'
        else:
            i = ids[0]
            videos[i].clips.append(clp)

with open(outfile, 'w') as f:
    line = ','.join([ 'id', 'ano', 'mes', 'dia', 'fecha', 'dia semana', 'bloque', 'materia', 'observador', 'nombre', 'apellido',
        'genero', 'posicion sala', 'hora', 'minutos', 'segundos', 'hora comienzo', 'clip a', 'clip b', 'clip c', 'clip d', 'clip e',
        'duracion total' ]) + '\n'
    f.write(line)
    for v in videos:
        line = ','.join([ v._id, v.date_time.strftime('%Y'), v.date_time.strftime('%m'), v.date_time.strftime('%d'), 
            v.date_time.strftime('%m/%d/%y'), dia[v.date_time.weekday()], v.block, '', v.observer, nombre[int(v.observer)], 
            apellido[int(v.observer)], genero[int(v.observer)], '',
            v.date_time.strftime('%H'), v.date_time.strftime('%M'), v.date_time.strftime('%S'), v.date_time.strftime('%H:%M:%S'),
            getClipDuration(v,'a'), getClipDuration(v,'b'), getClipDuration(v,'c'), getClipDuration(v,'d'), getClipDuration(v,'e'),
            '' ]) + '\n'
        f.write(line)