### bead diameters are addressed in BeadList, not in this class
class Bead:
    ### Custom constructor for Bead class
    def __init__(self, bead_ID_, xCoordinate_, yCoordinate_):
        ### Assign member variables
        self.ID = bead_ID_ # Number which identifies a specific Bead object
        self.leftmost = xCoordinate_ # The leftmost pixel coordinate of the space covered by this Bead object
        self.topmost = yCoordinate_ # The topmost pixel coordinate of the space covered by this Bead object
        self.color = None

        ### These values are only set if colorMatch is set (if colorMatch == True)
        self.matchedColorName = None
        self.matchedColorBrand = None
        self.matchedColorProductCode = None
    
    ### Recolors the Bead object's color. Casts to int in case rgb values are floats
    def recolorBead(self, r, g, b):
        r = int(r)
        g = int(g)
        b = int(b)
        self.color = (r, g, b) 