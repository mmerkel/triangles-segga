import sys

from PyQt4.QtCore import QSizeF, QPointF, Qt
from PyQt4.QtGui import QImage, QPrinter, QPainter, QApplication, QPen, QBrush, QPolygonF, QFont
from numpy import array

from Geometry.Point import Point


class PdfFile:
    Offset = array([0.5, 0.5])
    App = QApplication(sys.argv)

    def __init__(self, filename, size):
        '''
        :param filename:  output pdf file name
        :param size:  EITHER a QSizeF structure, OR the path of a raster image file, which will be put into the background of the pdf
        '''
        self.img = None
        if isinstance(size, QSizeF):
            self.size = size
        else:
            self.img = QImage()
            self.img.load(size)
            self.size = QSizeF(self.img.size())

        self.printer = QPrinter()
        self.printer.setPaperSize(self.size, QPrinter.DevicePixel)
        self.printer.setFullPage(True)
        self.printer.setColorMode(QPrinter.Color)
        self.printer.setOutputFileName(filename)

        self.painter = QPainter()
        self.painter.begin(self.printer)
        if not self.img is None:
            self.painter.drawImage(0, 0, self.img)
        self.painter.setRenderHint(QPainter.Antialiasing, True)


    def save(self):
        self.painter.end()

    def toQPointF(self, point):
        offsetPoint = point + PdfFile.Offset
        return QPointF(offsetPoint[0], offsetPoint[1])

    def drawCircle(self, point, radius, color):
        self.painter.setPen(QPen(Qt.NoPen))
        self.painter.setBrush(QBrush(color))
        self.painter.drawEllipse(self.toQPointF(point), radius, radius)

    def drawPolygon(self, pointList, fillColor, outlineColor=None, outlineWidth=None):
        if outlineColor is None:
            self.painter.setPen(QPen(Qt.NoPen))
        else:
            self.painter.setPen(QPen(QBrush(outlineColor), outlineWidth))
        self.painter.setBrush(QBrush(fillColor))
        poly = QPolygonF()
        for p in pointList:
            poly.append(self.toQPointF(p))
        self.painter.drawPolygon(poly)

    def drawLine(self, p1, p2, color=None, width=None):
        self.painter.setPen(QPen(QBrush(color), width))
        self.painter.drawPolygon(self.toQPointF(p1), self.toQPointF(p2))

    def drawText(self, position, text, pixelSize, color=Qt.white):
        font = QFont(self.painter.font())
        font.setPixelSize(pixelSize)
        self.painter.setPen(color)
        self.painter.setFont(font)
        self.painter.drawText(self.toQPointF(position), text)

if __name__=="__main__":
    pdf = PdfFile("output/test03.pdf", "output/test02.png")
    pdf.drawCircle(Point(10, 10), 0.5, Qt.red)
    pdf.save()
