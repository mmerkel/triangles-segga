from random import randint

from PyQt4.QtGui import QColor
from numpy import array, cos, sin, exp


def drawCellWithRandomColor(pdf, cell, fillAlpha=0x40, width=0.3, centerRadius=2):
    pointList = [e.vertex.position for e in cell.edges]
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    pdf.drawPolygon(pointList, fillColor=QColor(r, g, b, fillAlpha), outlineColor=QColor(r, g, b), outlineWidth=width)
    if not centerRadius is None:
        pdf.drawCircle(cell.baryCenter, centerRadius, QColor(r, g, b))

def drawNetwork(pdf, network, **kwargs):
    for cell in network.cells:
        drawCellWithRandomColor(pdf, cell, **kwargs)

def drawTriangles(pdf, triangles, fillColor=QColor(0xFF, 0, 0, 0x40), outlineColor=QColor(0xFF, 0, 0), outlineWidth=0.4, cornerColor=QColor(0, 0xFF, 0, 0x40), cornerRadius=2):
    if not cornerColor is None:
        allCorners = []
        for t in triangles:
            allCorners.append(t.p1)
            allCorners.append(t.p2)
            allCorners.append(t.p3)
        for c in allCorners:
            pdf.drawCircle(c, cornerRadius, cornerColor)
    for t in triangles:
        pdf.drawPolygon([t.p1, t.p2, t.p3], fillColor=fillColor, outlineColor=outlineColor, outlineWidth=outlineWidth)

def drawNematic(pdf, center, nematic, scaling=10, color=QColor(0, 0, 0xFF, 0xFF), width=1):
    deltaNorm = 0.5*scaling*nematic.norm()
    # print(deltaNorm, nematic.norm())
    angle = nematic.angle()
    delta = deltaNorm*array([cos(angle), sin(angle)])
    pdf.drawLine(center-delta, center+delta, color, width)

def drawNematicExp(pdf, center, nematic, scaling=1, color=QColor(0, 0, 0xFF, 0xFF), width=1):
    deltaNorm = 0.5*scaling*exp(2*nematic.norm())
    # print(deltaNorm, nematic.norm())
    angle = nematic.angle()
    delta = deltaNorm*array([cos(angle), sin(angle)])
    pdf.drawLine(center-delta, center+delta, color, width)
