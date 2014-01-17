import numpy as np
import xlwt

class result(object):
    def __init__(self, title=None, hheaders=None, vheaders=None, data=None):
        self.title = title
        self.hheaders = hheaders
        self.vheaders = vheaders
        self.data = data

    def disp(self):
        print self.title
        print self.hheaders
        print self.vheaders
        print self.data

    def toExcel(self, filename):
        wb = xlwt.Workbook()
        sh = wb.add_sheet(self.title)

        titleFont = xlwt.Font()
        titleFont.bold = True
        titleStyle = xlwt.XFStyle()
        titleStyle.font = titleFont

        perStyle = xlwt.XFStyle()
        perStyle.num_format_str = '0.00%'

        centerAlignment = xlwt.Alignment()
        centerAlignment.horz = xlwt.Alignment.HORZ_CENTER
        hyphenStyle = xlwt.XFStyle()
        hyphenStyle.alignment = centerAlignment

        sh.write(0, 0, self.title, titleStyle)
        
        nList = len(self.data)
        posx = 0
        for l in xrange(nList):
            currentHHeaders = self.hheaders[l]
            currentVHeaders = self.vheaders[l]
            currentData = self.data[l]
            sh.write(2+posx, 0, currentHHeaders[0], titleStyle)
            n1 = len(currentVHeaders)
            n2 = len(currentHHeaders)-1
            if n1 == 1:
                currentData.shape = (1,len(currentData))
            for i in xrange(n1):
                sh.write(i+3+posx, 0, currentVHeaders[i])
                for j in xrange(n2):
                    if i == 0:
                        sh.write(2+posx, j+1, currentHHeaders[j+1])
                    #if i==j:
                    #    sh.write(i+3+posx, j+1, '-', hyphenStyle)
                    #else:
                    #    sh.write(i+3+posx, j+1, currentData[i][j], perStyle)
                    sh.write(i+3+posx, j+1, currentData[i][j])
            posx += n1+2
        wb.save(filename)
