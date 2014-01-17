import numpy as np

class prop(object):
    def __init__(self, name, columns, excelSheet):
        self.name = name
        self.columns = columns
        self.reviewers = []
        self.setData(columns, excelSheet)

    def setData(self, columns, sh):
        nReviewers = len(columns)
        reviewers = []
        nVideos = len(sh.col_values(0)[1:])

        data = np.empty([nReviewers, nVideos], dtype=int)
        #iterate through Reviewers
        i = 0
        for idRev, colList, actions in columns:
            reviewers.append(idRev)
            dataCols = np.array([sh.col_values(col)[1:] for col in colList])
            for action in actions:
                if action == 'delta':
                    dataCols = dataCols > 0
                elif action == 'delta10':
                    dataCols = dataCols > 10
                elif action == 'delta4':
                    dataCols = dataCols > 4
                elif action == 'sum':
                    dataCols = np.sum(dataCols, 0)
                elif action == 'countUnique':
                    dataCols = dataCols.T
                    dataCols = np.array([len(np.unique(row))-1 if 99 in row else len(np.unique(row)) for row in dataCols])
                else:
                    print "error con las acciones"
                    raise
            data[i] = dataCols
            i += 1
        self.reviewers = reviewers
        self.data = data

    def getData(self):
        return self.data

    def getName(self):
        return self.name

    def getColumns(self):
        return self.columns

    def getReviewers(self):
        return self.reviewers

    def getRevIndex(self, idRev):
        return self.reviewers.index(idRev)

    def getDatum(self, idRev, vid):
        rev = self.getRevIndex(idRev)
        if vid == ':':
            return self.data[rev]
        else:
            return self.data[rev][vid]

    def add(self, prop2):
        self.columns.extend(prop2.getColumns())
        self.reviewers.extend(prop2.getReviewers())
        self.data = np.vstack((self.data, prop2.getData()))
