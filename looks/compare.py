import sys

file1 = 'avelio.csv'
file2 = sys.argv[1]

cols1 = [1,3,4] #id, bloque, dia de la semana
cols2 = [1,8,7]

ids = range(37)
weekdays = range(6)[1:]

def mix(l1, l2):
    l = []
    for i in xrange(len(l1)):
        l.append(l1[i])
        l.append(l2[i])
    return l

def nObs(filename, cols, ids, weekdays):
    n = {i:0 for i in ids}
    nByWeekday = {i:{w:0 for w in weekdays} for i in ids}
    blocksToFilter = ['None', 'r1', 'r2', 'al']
    with open(filename, 'r') as f:
        for row in f.readlines()[1:]:
            row = row.replace('\n','').split(',')
            if row[cols[1]] in blocksToFilter: continue
            curId = int(row[cols[0]])
            curWeekday = int(row[cols[2]])
            n[curId] += 1
            nByWeekday[curId][curWeekday] += 1
    return n, nByWeekday
            
nObs1, nByWeekday1 = nObs(file1, cols1, [i+1 for i in ids], weekdays)
nObs2, nByWeekday2 = nObs(file2, cols2, ids, weekdays)

out = 'comparacion_' + file2[:-4] + '.csv'
with open(out, 'w') as o:
    l = ['id', 'n' + file1, 'n' + file2]
    l.extend(mix([str(w) + '_' + file1 for w in weekdays], [str(w) + '_' + file2 for w in weekdays]))
    l = ','.join(l) + '\n'
    o.write(l)
    for i in xrange(len(ids)):
        curId = ids[i]
        n1 = nObs1[curId+1]
        n2 = nObs2[curId]
        byWeekday1 = [nByWeekday1[curId+1][w] for w in weekdays]
        byWeekday2 = [nByWeekday2[curId][w] for w in weekdays]
        byWeekday = mix(byWeekday1, byWeekday2)
        l = [curId, n1, n2]
        l.extend(byWeekday)
        l = [str(i) for i in l]
        l = ','.join(l) + '\n'
        o.write(l)
