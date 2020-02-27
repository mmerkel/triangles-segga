import scipy.io as sio

from Network import Network

MaxNVertices = 1000

def loadFromFile(path):
    '''
    :param path: path to .mat output file from SEGGA
    :return: Network structure
    '''

    mat = sio.loadmat(path)
    vertexCellArray = mat["cellgeom"]["nodecellmap"][0][0]
    vertexPositions = mat["cellgeom"]["nodes"][0][0]

    # x and y coordinates are flipped, so:
    realvertexPositions = vertexPositions[:,::-1]

    # start cell & vertex indices at zero like in a decent programming language
    vertexCellArray -= 1

    return _networkFromNodeData(vertexCellArray, realvertexPositions)

def _networkFromNodeData(vertexCellArray, vertexPositions):
    '''
    :param vertexCellArray: Ex2 array with E being the number of directed edges; first column: cell id (starting at zero!), second column: node id (starting at zero!)
    :param vertexPositions: Vx2 array with V being the number of vertices; first column: x coordinate, second column: y coordinate
    :return: Network structure
    '''

    network = Network()


    # create all elements
    vertexDict = {}
    lastCellId = None
    for cellId, vertexId in vertexCellArray:
        if cellId != lastCellId:
            # new cell:
            cell = network.addCell()
            cell.seggaLoadId = cellId+1

        # check if vertex already exists
        if vertexId in vertexDict:
            vertex = vertexDict[vertexId]
        else:
            vertex = network.addVertex(vertexPositions[vertexId])
            vertexDict[vertexId] = vertex
        # put the vertexId into the vertex, needed for the wiring later
        # collision danger, so more complicated variable name
        vertex.seggaLoadId = vertexId+1

        # create directed edge
        edge = network.addDirectedEdge(cell, vertex)

        # append edge to cell, prepend to ensure ccw ordering, note that the y coordinates are from top to bottom
        cell.edges.insert(0, edge)

        lastCellId = cellId

    # wire the edges amongst themselves
    edgeDict = {}
    for cell in network.cells:
        if len(cell.edges)<2:
            raise Exception("Only %d edges around cell %d!"%(len(cell.edges), cell.seggaLoadId))

        lastEdge = cell.edges[-1]
        for edge in cell.edges:
            edge.previousEdgeAroundCell = lastEdge

            # connect to twin
            curVid = edge.vertex.seggaLoadId
            lastVid = lastEdge.vertex.seggaLoadId
            lastEdge.seggaLoadId = (lastVid, curVid)
            edgeDict[lastEdge.seggaLoadId] = lastEdge

            # check whether the twin is already there and wire if so:
            indexTwinOfLastEdge = (curVid, lastVid)
            if indexTwinOfLastEdge in edgeDict:
                twin = edgeDict[indexTwinOfLastEdge]
                lastEdge.twin = twin
                twin.twin = lastEdge

            lastEdge = edge


    # finally, wire the vertices:
    vertexDone = {}
    for cell in network.cells:
        for edge in cell.edges:
            vertex = edge.vertex
            if not vertex.seggaLoadId in vertexDone:
                nextEdge = edge
                while True:
                    vertex.edges.append(nextEdge)
                    nextEdge = nextEdge.previousEdgeAroundCell.twin
                    if nextEdge is None:
                        vertex.edges = None
                        break
                    if nextEdge.vertex.seggaLoadId != vertex.seggaLoadId:
                        raise Exception("Swiched vertex when trying to walk around vertex %d!"%vertex.seggaLoadId)
                    if nextEdge == edge:
                        break
                    if len(vertex.edges)>MaxNVertices:
                        print(vertex.edges)
                        raise Exception("More than %d edges around vertex %d!"%(MaxNVertices, vertex.seggaLoadId))
                vertexDone[vertex.seggaLoadId] = None

    network.computeCellCenters()
    return network


if __name__=="__main__":
    network = loadFromFile("data/20171010_s_T0001_new_Z0001.mat")
