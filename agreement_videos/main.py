from review import review
import numpy as np
from result import result

if __name__ == '__main__':

    excelFile = '/home/johan/proyectos/agreement_videos/PlanillaRevisionErrorManuela_16Abril.xlsx'
    #lista de pares (nombre, lista de pares (revisor, lista de columnas))
    properties = []
    
    name = 'numFaces' 
    columns = [('Viviana', [6,8,10,12], ['delta','sum']), ('Ximena', [15,17,19,21], ['delta','sum'])]
    c = [28,41,54,67,87,100,113,126,146,159,172,185,205,218,231,244,264,277,290,303,323,336,349,362,382,395,408,421,441,453,466,479]
    c.extend([499,511,524,537,557,570,583,596,616,629,642,655,675,687,700,713])
    columns.extend([('Manuela', c, ['countUnique'])])
    c = [81,82,83,84,140,141,142,143,199,200,201,202,258,259,260,261,317,318,319,320,376,377,378,379,435,436,437,438,493,494,495,496]
    c.extend([551,552,553,554,610,611,612,613,669,670,671,672,727,728,729,730])
    columns.extend([('Picassa', c, ['countUnique'])])
    properties.append((name, columns))
    
    name = 'hayCara'
    columns = [('Viviana', [5], []), ('Ximena', [14], []), ('EmocionesCIAE', [23], ['delta','sum']), ('Manuela', [25], ['delta','sum'])]
    columns.extend([('Picassa', [80,139,198,257,316,375,434,492,550,609,668,726], ['sum','delta'])])
    properties.append((name, columns))

    rev = review(excelFile, properties)

    excelRagnar = '/home/johan/proyectos/agreement_videos/PlanillaRevisionErrorRagnar_16Abril.xlsx'
    properties = []

    name = 'hayCara'
    columns = [('Ragnar', [25], ['delta','sum'])]
    properties.append((name, columns))

    name = 'numFaces' 
    c = [28,41,54,67,87,100,113,126,146,159,172,185,205,218,231,244,264,277,290,303,323,336,349,362,382,395,408,421,441,453,466,479]
    c.extend([499,511,524,537,557,570,583,596,616,629,642,655,675,687,700,713])
    columns = [('Ragnar', c, ['countUnique'])]
    properties.append((name, columns))

    rev2 = review(excelRagnar, properties)

    rev.add(rev2)

    excelOpenCV = '/home/johan/proyectos/agreement_videos/n_photos_opencv.xlsx'
    properties = []

    name = 'hayCara'
    columns = [('OpenCV', [1], ['delta4','sum'])]
    properties.append((name, columns))

    rev3 = review(excelOpenCV, properties)
    rev.add(rev3)

    #print rev.agreement('hayCara', ['Viviana', 'Manuela'], '%')
    headers11 = ['Acuerdo']
    headers12 = ['Desacuerdo']
    headers1 = rev.getReviewers('hayCara', names=1)
    headers11.extend(headers1)
    headers12.extend(headers1)
    data11 = rev.agreement('hayCara', ':', '%')
    data12 = rev.disagreement('hayCara', ':', '%')
    res1 = result('Hay al menos una cara', [headers11, headers12], [data11, data12])
    res1.toExcel('hayCara.xls') 
    #print rev.videosOfDisagreement('hayCara', ['EmocionesCIAE_M', 'EmocionesCIAE_R'])
    headers21 = ['Acuerdo']
    headers22 = ['Desacuerdo']
    headers2 = rev.getReviewers('numFaces', names=1)
    headers21.extend(headers2)
    headers22.extend(headers2)
    data21 = rev.agreement('numFaces', ':', '%')
    data22 = rev.disagreement('numFaces', ':', '%')
    res2 =  result('No. de Caras', [headers21, headers22], [data21, data22])
    res2.toExcel('numCaras.xls')

    print rev.videosOfDisagreement('hayCara',['Ximena','OpenCV'])
