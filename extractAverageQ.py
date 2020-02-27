import os
from numpy import sqrt
import Segga
from Drawing import PdfFile
from Geometry.Point import Point
from Geometry.triangleProperties import computeAreaAndElongationNematic
from Network import createTriangleList
from NetworkDrawing import drawNetwork, drawTriangles, drawNematic

Mask = "20171010_s_T%04d_new_Z0001"
for number in range(1, 162):
    Id = Mask%number
    OutputFolder = "output/all/%s/"%Id
    try:
        os.makedirs(OutputFolder)
    except:
        pass
    print("Writing to %s..."%OutputFolder)

    try:
        network = Segga.loadFromFile("data/%s.mat"%Id)
        triangles = createTriangleList(network)
    except:
        continue

    # pdf = PdfFile(OutputFolder + "cells.pdf", "data/%s.tif"%Id)
    # drawNetwork(pdf, network)
    # pdf.save()
    #
    # pdf = PdfFile(OutputFolder + "triangles.pdf", "data/%s.tif"%Id)
    # drawTriangles(pdf, triangles)
    # pdf.save()


    qNormSum, qxxSum, qxySum, areaSum = 0, 0, 0, 0
    for triangle in triangles:
        area, q = computeAreaAndElongationNematic(triangle)
        qNormSum += area*q.norm()
        qxxSum += area*q.xx
        qxySum += area*q.xy
        areaSum += area
    AvgQNorm = qNormSum/areaSum
    Qxx = qxxSum/areaSum
    Qxy = qxySum/areaSum
    Q = sqrt(Qxx**2+Qxy**2)
    print("Q (norm of average) = %.3f"%Q)
    print("Q (average of norm) = %.3f"%AvgQNorm)
    print("Q (alignment part)  = %.3f"%(Q/AvgQNorm))


    # pdf = PdfFile(OutputFolder + "trianglesAndBars.pdf", "data/%s.tif"%Id)
    # drawTriangles(pdf, triangles)
    # for triangle in triangles:
    #     area, q = computeAreaAndElongationNematic(triangle)
    #     drawNematic(pdf, triangle.center(), q, scaling=30)
    # pdf.drawText(Point(10, 30), "Qxx = %.3f"%Qxx, 18)
    # pdf.drawText(Point(10, 50), "Qxy = %.3f"%Qxy, 18)
    # pdf.drawText(Point(10, 70), "Q = %.3f"%Q, 18)
    # pdf.save()
