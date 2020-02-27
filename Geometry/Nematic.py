from numpy import *

class Nematic:
    def __init__(self, xx=0, xy=0):
        self.xx=xx
        self.xy=xy
    def angle(self):
        return 0.5*arctan2(self.xy, self.xx)
    def norm(self):
        return sqrt(self.xx**2 + self.xy**2)
    def __str__(self):
        return "Nematic(%g, %g)"%(self.xx, self.xy)