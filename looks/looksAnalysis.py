from datetime import datetime, timedelta, time
import numpy as np
import scipy.sparse as sp
import pickle, os, glob

def allIndices(value, List):
    return [i for i in range(len(List)) if List[i]==value]

def unionList(List):
    #input is a list of lists
    #returns a list with the union of the elements of the lists
    u = set
    for l in List:
        u = u.union(set(l))
    return sorted(list(u))

def str2float(s):
    try:
        s = float(s)
    except:
        s = None
    return s

def unique(seq): 
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def removeNones(l):
    l = [e for e in l if not e is None]
    return l

class look(object):
    def __init__(self, interaction=None, observer=None, observed=None, date_time=None, block=None, subject=None):
        self.interaction = interaction
        self.observer = observer
        self.observed = observed        
        self.date_time = date_time
        self.block = block
        self.subject = subject

class rut(object):
    def __init__(self, *args):
        if len(args) == 1: self.__setup1(*args)
        elif len(args) == 2: self.__setup2(*args)
        
    def  __setup1(self, string):
        #format 12.345.678-9 or 12345678-9 or 123456789
        string = string.replace('.','')
        string = string.replace('-','')
        self.number = int(string[:-1])
        self.vd = str.lower(string[-1])

    def  __setup2(self, number, vd):
        self.number = number
        self.vd = str.lower(str(vd))

    def toStr(self):
        return str(self.number) + '-' + self.vd

class person(object):
    def __init__(self, _id=None, names=None, lastname1=None, lastname2=None, gender=None, rut=None, role=None, evaluation=None, grades=None):
        self._id = _id
        self.names = names
        self.lastname1 = lastname1
        self.lastname2 = lastname2
        self.gender = gender
        self.rut = rut
        self.role = role
        self.evaluation = evaluation
        self.grades = grades
        #artes, ciencias, ed. fisica, historia, lenguaje, matematicas, tecnologia

    def getMean(self, listName):
        if listName == 'evaluation':
            l = self.evaluation
        elif listName == 'grades':
            l = self.grades
        else:
            l = []
        if len(l) > 0:
            l = removeNones(l)
            m = np.mean(l)
        else:
            m = None
        return m

class timetable(object):
    def __init__(self, tt=None, blocks=None):
        self.tt = tt
        self.blocks = blocks

        if self.blocks is None:
            self.blocks = {}
        if self.tt is None:
            self.tt = {0:self.genEmptyTTDay(), 1:self.genEmptyTTDay(), 2:self.genEmptyTTDay(), 3:self.genEmptyTTDay(), 4:self.genEmptyTTDay()}

    def genEmptyTTDay(self):
        return {key:None for key in self.blocks.keys()}

    def getBlock(self, time):
        for key in self.blocks.iterkeys():
            if self.blocks[key][0] <= time < self.blocks[key][1]:
                return key
        return None

    def getSubject(self, date_time):
        try:
            day = date_time.weekday()
            block = self.getBlock(date_time.time())
            ans = self.tt[day][block]
        except:
            ans = None
        return ans

    def getTimes(self, block):
        return (self.blocks[block][0], self.blocks[block][1])

    def setTT(self, filename):
        with open(filename,'r') as f:
            for row in f.readlines():
                row = row.replace('\n','').split(',')
                block = row[0]
                for day in xrange(5):
                    self.tt[day][block] = row[day+1]

    def setBlocks(self, filename):
        with open(filename,'r') as f:
            for row in f.readlines():
                row = row.replace('\n','').split(',')
                self.blocks[row[0]] = [datetime.strptime(row[1], '%X').time(), datetime.strptime(row[2], '%X').time()]

class clip(object):
    def __init__(self, _id, duration):
        self._id = _id
        self.duration = duration

class video(object):
    def __init__(self, _id=None, date_time=None, block=None, subject=None, observer=None, roomPos=None, clips=None, duration=None):
        self._id = _id
        self.date_time = date_time
        self.block = block
        self.subject = subject
        self.observer = observer
        self.roomPos = roomPos
        self.clips = clips
        self.duration = duration

        if self.clips is None:
            self.clips = []

    def getClip(self, clipId):
        clip = [c for c in self.clips if c._id == clipId]
        return clip[0]

    def getClipDatetime0(self, clipId):
        part = clipId.split('_')[-1]
        if part == 'a':
            delta = 0
        elif part == 'b':
            delta = self.clips[0].duration
        elif part == 'c':
            delta = self.clips[0].duration + self.clips[1].duration
        elif part == 'd':
            delta = self.clips[0].duration + self.clips[1].duration + self.clips[2].duration
        delta = timedelta(seconds=delta)
        return self.date_time + delta

class looksAnalysis(object):
    def __init__(self, filename=None):
        self.exactLooks = []
        self.looks = []
        self.people = []
        self._timetable = timetable()
        self.videos = []

        if not filename is None:
            self.load(filename)

    def matlab2numpy(self, filename, sparse=False):
        with open(filename,'r') as f:
            s=f.read()
            s=s.replace(']  [','] , [')
            s=s.replace('[','np.array([[')
            s=s.replace(']',']])')
            s=s.replace(';','],[')
            s=s.replace('{','[')
            s=s.replace('}',']')
            exec s in globals()

        if sparse:            
            for i in xrange(len(A)):
                A[i] = sp.dok_matrix(A[i])

        return A

    def getObserverIds(self, matrices, date_time, delta, useVideos=False):
        if useVideos:
            blocks = []
            observerIds = []
            for m in matrices:
                block = self.getBlock(date_time.time())
                I = []
                for video in self.videos:
                    if date_time.date() == video.date_time.date() and block == video.block:
                        I.append(int(video.observer._id))
                observerIds.append(I)
                blocks.append(block)
                date_time += delta
        else:
            blocks = []
            observerIds = []
            for m in matrices:
                if len(m.keys()) == 0:
                    I = []
                else:
                    I, J = zip(*m.keys())
                    I = np.unique(I)
                block = self.getBlock(date_time.time())
                observerIds.append(I)
                blocks.append(block)
                date_time += delta

            allBlocks = np.unique(blocks)
            for b in allBlocks:
                indices = allIndices(b, blocks)
                auxObserverIds = [observerIds[i] for i in indices]
                blockObserverIds = unionList(auxObserverIds)
                for i in indices:
                    observerIds[i] = blockObserverIds
            #agregar los de los recreos en los anteriores
            breaks = ['r1', 'r2', 'al']
            previous = ['1_2', '3_4', '5_6']
            next = ['3_4', '5_6', '7_8']
            for b in allBlocks:
                if b in breaks:
                    prev = previous[breaks.index(b)]
                    nxt = next[breaks.index(b)] 
                    breakIndices = allIndices(b, blocks)
                    breakObservers = observerIds[breakIndices[0]]

                    breakMatrices = [matrices[i] for i in breakIndices]
                    #para cada alumno miro si tuvo interacciones en la primera o segunda mitad del recreo
                    for h in breakObservers:
                        interactions = [self.getInteraction(m, h) for m in breakMatrices]
                        midPoint = len(interactions)/2
                        if np.sum(interactions[:midPoint]) > 0:
                            indices = allIndices(prev, blocks)
                            newBlockObserverIds = unionList([observerIds[indices[0]], [h]])
                            for i in indices:
                                observerIds[i] = newBlockObserverIds
                        if np.sum(interactions[midPoint:]) > 0:
                            indices = allIndices(nxt, blocks)
                            newBlockObserverIds = unionList([observerIds[indices[0]], [h]])
                            for i in indices:
                                observerIds[i] = newBlockObserverIds
        return observerIds, blocks

    def getObservers(self, date_time0, date_time1, delta, useVideos):
        if useVideos:
            blocks = []
            observers = []
            while date_time0 < date_time1:
                block = self.getBlock(date_time0.time())
                O = []
                for video in self.videos:
                    if date_time0.date() == video.date_time.date() and block == video.block:
                        O.append(video.observer)
                observers.append(O)
                blocks.append(block)
                date_time0 += delta
        else:
            blocks = []
            while date_time0 < date_time1:
                block = self.getBlock(date_time0.time())
                blocks.append(block)
                date_time0 += delta

            allBlocks = np.unique(blocks)
            observers = range(len(blocks))
            for b in allBlocks:
                indices = allIndices(b, blocks)
                times = self.getTimes(b)
                dt0 = datetime.combine(date_time0.date(), times[0])
                dt1 = datetime.combine(date_time0.date(), times[1])
                blockObservers = self.getObsFromExactLooks(dt0, dt1)
                for i in indices:
                    observers[i] = blockObservers
            #agregar los de los recreos en los anteriores
            breaks = ['r1', 'r2', 'al']
            previous = ['1_2', '3_4', '5_6']
            next = ['3_4', '5_6', '7_8']
            for b in allBlocks:
                if b in breaks:
                    prev = previous[breaks.index(b)]
                    nxt = next[breaks.index(b)] 
                    breakIndices = allIndices(b, blocks)
                    breakObservers = observers[breakIndices[0]]

                    #para cada alumno miro si tuvo interacciones en la primera o segunda mitad del recreo
                    #optimizar
                    for o in breakObservers:
                        dts = []
                        t0, t1 = self.getTimes(b)
                        dt0 = datetime.combine(date_time0.date(), t0)
                        dt1 = datetime.combine(date_time0.date(), t1)
                        dt = dt0
                        while dt < dt1:
                            dts.append((dt, dt+delta))
                            dt += delta
                        interactions = [self.getInteraction2(o, dt0, dt1) for dt0, dt1 in dts]
                        midPoint = len(interactions)/2
                        if np.sum(interactions[:midPoint]) > 0:
                            indices = allIndices(prev, blocks)
                            newBlockObservers = unionList([observers[indices[0]], [o]])
                            for i in indices:
                                observers[i] = newBlockObservers
                        if np.sum(interactions[midPoint:]) > 0:
                            indices = allIndices(nxt, blocks)
                            newBlockObservers = unionList([observers[indices[0]], [o]])
                            for i in indices:
                                observers[i] = newBlockObservers
        return observers, blocks

    def getObsFromExactLooks(self, dt0, dt1):
        obs = unique([el.observer for el in self.exactLooks if el.date_time >= dt0 and el.date_time < dt1])
        return obs

    def getInteraction(self, matrix, observerId):
        if matrix.getrow(observerId).sum() > 0:
            ans = 1
        else:
            ans = 0
        return ans

    def getInteraction2(self, o, dt0, dt1):
        observed = [ el.observed for el in self.exactLooks if el.date_time >= dt0 and el.date_time < dt1 and el.observer == o ]
        if len(observed) > 0:
            interaction = 1
        else:
            interaction = 0
        return (interaction, observed)

    def getSubject(self, date_time):
        return self._timetable.getSubject(date_time)

    def getBlock(self, time):
        return self._timetable.getBlock(time)

    def getTimes(self, block):
        return self._timetable.getTimes(block)

    def getPerson(self, _id):
        for person in self.people:
            if person._id == _id:
                return person
        return None

    def setLooks(self, fileList, delta, useVideos=False):
        delta = timedelta(seconds=delta)
        with open(fileList, 'r') as fl:
            for row in fl.readlines():
                row = row.replace('\n','').split(',')
                date_time = datetime.strptime(row[1], '%x %X') #09/26/12 08:30:00
                filename = row[0]
                matrices = self.matlab2numpy(filename, sparse=True)
                observerIds, blocks = self.getObserverIds(matrices, date_time, delta, useVideos)
                for m, hIds, bl in zip(matrices, observerIds, blocks):
                    for hId in hIds:
                        interaction = self.getInteraction(m, hId)
                        subject = self.getSubject(date_time)
                        self.looks.append(look(interaction, self.people[hId], date_time, bl, subject))
                    date_time += delta

    def setLooks2(self, datetimeList, delta, useVideos=False):
        delta = timedelta(seconds=delta)
        for date_times in datetimeList:
            observers, blocks = self.getObservers(date_times[0], date_times[1], delta, useVideos)
            date_time = date_times[0]
            for obs, block in zip(observers, blocks):
                for ob in obs:
                    (interaction, observed) = self.getInteraction2(ob, date_time, date_time+delta)
                    subject = self.getSubject(date_time)
                    if len(observed)>0:
                        for obd in observed:
                            self.looks.append(look(interaction, ob, obd, date_time, block, subject))    
                    else:
                        self.looks.append(look(interaction, ob, 'None', date_time, block, subject))
                date_time += delta

    def setExactLooks(self, folderList, frameRate):
        with open(folderList, 'r') as fl:
            for row in fl.readlines():
                folderPath = row.replace('\n','')
                parts = os.path.split(folderPath)
                folder = parts[-1]
                observer, date_time_0 = self.foldername2data(folder)
                for filename in glob.glob(os.path.join(folderPath, '*.jpg')):
                    filename = os.path.split(filename)[-1]
                    delta, observed = self.filename2data(filename, frameRate)
                    date_time = date_time0 + delta
                    block = self.getBlock(date_time.time())
                    subject = self.getSubject(date_time)
                    self.exactLooks.append(look(1, observer, observed, date_time, block, subject))
        self.removeDuplicateExactLooks() #aparecen cuando no se distingue a quien se vio o cuando los dos clasificadores detectaron la cara


    def setPeople(self, filename):
        with open(filename,'r') as f:
            for row in f.readlines()[1:]:
                row = row.replace('\n','').split(',')
                _id = row[0]
                nms = row[1]
                ln1 = row[2]
                ln2 = row[3]
                gdr = row[4]
                evs = self.setEvs(row[5:42])
                grs = self.setEvs(row[43:])
                self.people.append(person(_id=_id, names=nms, lastname1=ln1, lastname2=ln2, gender=gdr, evaluation=evs, grades=grs))

    def setTimetable(self, fileTT, fileBlocks):
        self._timetable.setBlocks(fileBlocks)
        self._timetable.setTT(fileTT)

    def setVideos(self, filename):
        col = {'id':0, 'date':4, 'time':16, 'block':6, 'subject':7, 'observer':8, 'roomPos':12, 'clip_a':17, 'clip_b':18, 'clip_c':19, 'clip_d':20, 'duration':21}
        with open(filename, 'r') as f:
            for row in f.readlines()[1:]:
                row = row.replace('\n','').split(',')
                date_time = datetime.strptime(row[col['date']] + ' ' + row[col['time']], '%x %X') #09/26/12 08:30:00
                _id = row[col['id']]
                clips = [clip(_id + '_a', row[col['clip_a']]), clip(_id + '_b', row[col['clip_b']]), clip(_id + '_c', row[col['clip_c']]), clip(_id + '_d', row[col['clip_d']])]
                observer = self.getPerson(row[col['observer']])
                self.videos.append(video(_id=_id, date_time=date_time, block=row[col['block']], subject=row[col['subject']], observer=observer, roomPos=row[col['roomPos']], clips=clips, duration=row[col['duration']]))

    def setEvs(self, l):
        return [str2float(s) for s in l]

    def foldername2data(self, folder):
        #ejemplo: 3_b_20121026100315_11_Nayareth.AVI
        fields = folder.split('_')
        videoId = '-'.join([ fields[2][:8], fields[0], fields[3] ])
        date_time = self.getVideo(videoId).getClipDatetime0( '_'.join([ videoId, fields[1] ]) )
        observer = self.people[int(fields[3])]
        return observer, date_time

    def filename2data(self, filename, frameRate):
        #ejemplo: 1_a_20121002082002_Nayareth.AVI_5_29040_29_VictorPoblete
        fields = filename.replace('.jpg','').split('_')
        #dt0 = datetime.strptime(fields[2], '%Y%m%d%H%M%S')
        frame = int(fields[5])
        seconds = frame/frameRate
        delta = timedelta(seconds=seconds)
        observed = self.people[int(fields[6])]
        return delta, observed

    def removeDuplicateExactLooks(self):
        l = [(el.interaction, el.observer, el.observed, el.date_time, el.block, el.subject) for el in self.exactLooks]
        l = unique(l)
        self.exactLooks = []
        for t in l:
            auxLook = look()
            auxLook.interaction = t[0]
            auxLook.observer = t[1]
            auxLook.observed = t[2]
            auxLook.date_time = t[3]
            auxLook.block = t[4]
            auxLook.subject = t[5]
            self.exactLooks.append(auxLook)

    def toCSV(self, filename, variable, attributes, headers):
        with open(filename, 'w') as f:
            l = ','.join(headers) + '\n'
            f.write(l)
            exec 'var = self.' + variable
            for v in var:
                l = []
                for att in attributes:
                    try:
                        exec 'a = str(v.' + att + ')'
                    except:
                        a = ''
                    l.append(a)
                l = ','.join(l) + '\n'
                f.write(l)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.__dict__ = pickle.load(f).__dict__
