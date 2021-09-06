import PIL
from PIL import Image
import numpy as np
from bead import Bead
from beadPattern import BeadPattern
import math

class ImageBeaderizer:
    ### Custom constructor for ImageBeaderizer class
    def __init__(self, beadPattern_, backgroundColor_): 
        self.beadDiameter = beadPattern_.beadDiameter
        beadList = beadPattern_.beadList

        ### Construct a blank image. This will be modified to produce a final image
        mode = "RGB"
        size = (beadPattern_.imageWidth, beadPattern_.imageHeight)
        color = backgroundColor_
        self.pictureOut = PIL.Image.new(mode, size, color)

        ### 
        self.beaderize(beadList, backgroundColor_)

       
    def beaderize(self, beadList, backgroundColor):
        for bead in beadList:
            xStart = bead.leftmost
            yStart = bead.topmost
            xCurrent = xStart
            yCurrent = yStart
            xFinal = xStart + bead.beadDiameter
            yFinal = yStart + bead.beadDiameter

            beadOuterRadius = bead.beadDiameter / 2
            beadInnerRadius = beadOuterRadius / 2

            centerX = bead.leftmost + beadOuterRadius
            centerY = bead.topmost + beadOuterRadius

            ### Iterates through the pixel space of size (beadDiameter by beadDiameter), starting with x = leftmost, y = topmost
            ### If the parsed pixel is "outside" the outer radius of the bead, the parsed pixel is set as backgroundColor_
            ### If the parsed pixel is inside the outer radius of the bead but outside the inner radius of the bead, the pixel color is set as bead.color 
            ### If the parsed pixel is inside the inner radius of the bead, the pixel color is set as backgroundColor_
            while xCurrent != xFinal:
                yCurrent = yStart
                while yCurrent != yFinal:
                    # "distance" is the distance between the center of the bead (i.e., the center of the pixel space) and the parsed pixel
                    distance = math.sqrt((xCurrent - centerX)**2 + (yCurrent - centerY)**2)
            
                    if distance >= beadInnerRadius and distance <= beadOuterRadius:
                        # If distance is greater than bead's inner radius and less than bead's outer radius, set its color as bead.color
                        self.pictureOut.putpixel((xCurrent, yCurrent), bead.color)
                    else:
                        # Set the parsed pixel as backgroundColor
                        self.pictureOut.putpixel((xCurrent, yCurrent), backgroundColor)

                    yCurrent = yCurrent + 1
                
                xCurrent = xCurrent + 1
    
    ### Prints the number total beads used. Also prints the dimensions of the final image in feet
    def printDimensions(self):
        self.beadRows = self.pictureOut.height / self.beadDiameter
        self.beadColumns = self.pictureOut.width / self.beadDiameter
        print("Total number of beads: " + str(round(self.beadRows * self.beadColumns)))

        # A physical bead is 5 mm (or 0.0164042 feet) in diameter
        widthInFeet = str(round((self.beadColumns * 0.0164042), 2))
        heightInFeet = str(round((self.beadRows * 0.0164042), 2))
        print("The output image is " + widthInFeet + " feet wide and " + heightInFeet + " feet wide")
