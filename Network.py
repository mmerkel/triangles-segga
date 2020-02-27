from numpy import array

from Geometry.triangleProperties import Triangle


class Network:
    class _Cell:
        def __init__(self):
            self.edges = [] # sorted in ccw sense
    class _DirectedEdge:
        def __init__(self, cell, vertex):
            self.cell = cell
            self.vertex = vertex # right vertex when looked from cell center
            self.twin = None # if this is None, it's the boundary of the tissue!
            self.previousEdgeAroundCell = None
            # self.nextEdgeAroundVertex = None
    class _Vertex:
        def __init__(self, position):
            self.position = position
            self.edges = [] # boundary edge is None
    def __init__(self):
        self.cells = []
        self.edges = []
        self.vertices = []
    def addCell(self):
        c = Network._Cell()
        self.cells.append(c)
        return c
    def addDirectedEdge(self, cell, vertex):
        e = Network._DirectedEdge(cell, vertex)
        self.edges.append(e)
        return e
    def addVertex(self, position):
        v = Network._Vertex(position)
        self.vertices.append(v)
        return v
    def computeCellCenters(self):
        for cell in self.cells:
            cell.area = 0
            cell.baryCenter = 0
            lastPosition = cell.edges[-1].vertex.position
            for edge in cell.edges:
                position = edge.vertex.position
                cell.area += lastPosition[0]*position[1] - lastPosition[1]*position[0]
                cell.baryCenter += (lastPosition[0]*position[1] - lastPosition[1]*position[0]) * (lastPosition+position)
                lastPosition = position
            cell.area /= 2
            cell.baryCenter /= 6*cell.area


def createTriangleList(network):
    triangles = []
    for vertex in network.vertices:
        if vertex.edges is None:
            continue

        if len(vertex.edges)<3:
            # raise Exception("Inner vertex has only %d edges attached to it!"%len(vertex.edges))
            print("Inner vertex has only %d edges attached to it!"%len(vertex.edges))
            continue

        cellCenters = array([e.cell.baryCenter for e in vertex.edges])
        if len(vertex.edges)==3:
            triangles.append(Triangle(cellCenters[0], cellCenters[1], cellCenters[2]))
        else:
            center = cellCenters.mean(axis=0)
            for i in range(len(vertex.edges)):
                triangles.append(Triangle(center, cellCenters[i-1], cellCenters[i]))

    return triangles