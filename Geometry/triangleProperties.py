from numpy import *

from Geometry.Nematic import Nematic


class Triangle:
    def __init__(self, p1, p2, p3):
        '''
        :param p1: Point 1 of triangle (numpy array of size 2: x, y)
        :param p2: Point 2 of triangle (numpy array of size 2)
        :param p3: Point 3 of triangle (numpy array of size 2)
        The three points are sorted in ccw order.
        '''
        self.p1, self.p2, self.p3 = p1, p2, p3
    def center(self):
        return (self.p1+self.p2+self.p3)/3

_Side0 = 2.0/sqrt(sqrt(3)) # side of a regular triangle with area 1
_RegularTriangleMatrix = _Side0*array([[-0.5*sqrt(3), -0.5*sqrt(3)], [0.5, -0.5]]) # the columns of this matrix are the two vectors r1-r0 and r2-r0; where ri are the corners of a regular triangle, sorted in ccw direction; the area of the triangle is 1.
_InverseRegularTriangleMatrix = linalg.inv(_RegularTriangleMatrix)

def computeAreaAndElongationNematic(tri):
    '''
    :param tri: triangle
    :return:  tuple of area (scalar) and elongation nematic (numpy array of size two: q_xx, q_xy)
    '''

    curTriangleMatrix = transpose([tri.p2-tri.p1, tri.p3-tri.p1])
    shape = dot(curTriangleMatrix, _InverseRegularTriangleMatrix)

    area = linalg.det(shape)
    linScalingFactor = sqrt(fabs(area))
    theta = arctan2(shape[1,0]-shape[0,1], shape[0,0]+shape[1,1])
    n = Nematic(xx=0.5*(shape[0,0]-shape[1,1]), xy=0.5*(shape[0,1]+shape[1,0]))
    twoPhi = theta + 2*n.angle()
    normQ = arcsinh(n.norm()/linScalingFactor)
    Q = Nematic(normQ*cos(twoPhi), normQ*sin(twoPhi))
    return area, Q
