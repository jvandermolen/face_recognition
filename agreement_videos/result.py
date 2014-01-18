import numpy as np
import xlwt

class result(object):
    def __init__(self, title, headers, data):
        self.title = title
        self.headers = headers
        self.data = data

    def disp(self):
        print self.title
        print self.headers
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
            currentHeaders = self.headers[l]
            currentData = self.data[l]
            sh.write(2+posx, 0, currentHeaders[0], titleStyle)
            n = len(currentHeaders)-1
            for i in xrange(n):
                sh.write(i+3+posx, 0, currentHeaders[i+1])
                sh.write(2+posx, i+1, currentHeaders[i+1])
                for j in xrange(n):
                    if i==j:
                        sh.write(i+3+posx, j+1, '-', hyphenStyle)
                    else:
                        sh.write(i+3+posx, j+1, currentData[i][j], perStyle)
            posx += n+2
        wb.save(filename)