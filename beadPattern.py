from RGB_Distance import RGB_Distance
import PIL
from PIL import Image
import numpy as np
from collections import Counter
import math
import pandas as pd
from pandas.core.series import Series
from bead import Bead
from RGB_Distance import *
import sys
import colorama
from colorama import Fore, Style
import rainbowString

class BeadPattern:
    ### Custom constructor for Picture class
    def __init__(self, sourceFilename_, beadDiameter_, colorscaleOutput_, transparentToColor_, backgroundColor_, beadColorMatch_, beadBrands_): 
        ### Assign member variables
        self.beadDiameter = beadDiameter_
        self.beadList = [] # The list to contain all the Bead objects
        self.imageWidth = None
        self.imageHeight = None
        self.beadRows = None # To be set as the number of rows of Beads in the final image
        self.beadColumns = None # To be set as the number of columns of Beads in the final image
        self.totalBeads = None
        self.outputImage = None


        sourceImage = self.preprocessing(sourceFilename_, transparentToColor_)
        
        self.buildBeadList(sourceImage)

        self.setDominantColor(sourceImage, colorscaleOutput_)

      
        if beadColorMatch_:
            if colorscaleOutput_:
                self.matchColorscale(beadBrands_)
            else:
                ### NOT YET WORKING
                self.matchGrayscale(beadBrands_)
        
        self.beadify(sourceImage.width, sourceImage.height, backgroundColor_)




    def preprocessing(self, sourceFilename, transparentToColor):

        def removeTransparentPixels(sourceImage):
            foregroundImage = sourceImage.convert("RGBA")

            # Create backgroundImage as image of a single color (color = transparentColor)
            backgroundImage = Image.new("RGBA", foregroundImage.size, transparentToColor)

            # Paste foregroundImage over backgroundImage
            backgroundImage.paste(foregroundImage, mask=foregroundImage)
            sourceImage = backgroundImage.convert("RGB") # Not necessary to convert to RGB, but it maintains consistency

            print("Preprocessing COMPLETED")
            return sourceImage


        def resizeSourceImage(sourceImage):

            width = sourceImage.width - (sourceImage.width % self.beadDiameter)
            height = sourceImage.height - (sourceImage.height % self.beadDiameter)

            if self.beadDiameter > width or self.beadDiameter > height:
                sys.exit(Fore.RED + "ERROR: The selected bead diameter is larger than one of the source image dimensions. Please select a smaller bead diameter. PROGRAM EXITED." + Style.RESET_ALL)


            sourceImage = sourceImage.resize((width, height))

            self.beadRows = int(height / self.beadDiameter)
            self.beadColumns = int(width / self.beadDiameter)
            self.totalBeads = self.beadRows * self.beadColumns

            return sourceImage

        
        def estimateRuntime():
            print("ESTIMATED RUNTIME: " + "XXX seconds")            


        sourceImage = Image.open(sourceFilename)
        sourceImage = removeTransparentPixels(sourceImage)
        sourceImage = resizeSourceImage(sourceImage)
        estimateRuntime()

        return sourceImage



    def buildBeadList(self, sourceImage):

        bead_ID = 0
        y = 0
        while y < sourceImage.height:
            x = 0
            while x < sourceImage.width:
                b = Bead(bead_ID, x, y)
                self.beadList.append(b)

                bead_ID += 1
                x += self.beadDiameter
            
            y += self.beadDiameter
    
        print("buildBeadList() COMPLETED")


    
    def setDominantColor(self, sourceImage, colorscaleOutput):
        for bead in self.beadList:
            r_Visited = []
            g_Visited = []
            b_Visited = []

            # Start the pixel iteration at the top left pixel of the Bead's pixel space
            xStart = bead.leftmost
            yStart = bead.topmost
            xCurrent = xStart
            yCurrent = yStart
            xFinal = xStart + self.beadDiameter
            yFinal = yStart + self.beadDiameter
          
            # Iterate through the Bead's pixel space and append RGB channel values
            rgb_Visited = []
            while yCurrent != yFinal:
                xCurrent = xStart
                while xCurrent != xFinal:
                    # Get the pixel's RGB channel values and append them to the _Visited lists
                    #print(xCurrent,yCurrent)
                    #print(sourceImage.width,sourceImage.height)
                    #rgb = sourceImage.getpixel((xCurrent, yCurrent))
                    rgb = sourceImage.getpixel((xCurrent, yCurrent))
                    rgb_Visited.append(rgb)
                    

                    xCurrent += 1
                
                yCurrent += 1

            # Construct Counter objects for each _Visited list
            rgb_Counter = Counter(rgb_Visited)

            # Determine the most common value for each of the RGB color channels
            rgb = rgb_Counter.most_common()
            r = rgb[0][0][0]
            g = rgb[0][0][1]
            b = rgb[0][0][2]
            

            if colorscaleOutput:
                bead.recolorBead(r, g, b)
            else:
                avg = (r + g + b) / 3
                bead.recolorBead(avg, avg, avg)
            

            
        print("setDominantColor() COMPLETED")


    def matchColorscale(self, beadBrands):
        realWorldBeads = pd.read_excel("Real_World Bead Data.xlsx")
        realWorldBeads = realWorldBeads.loc[(realWorldBeads["Brand"].isin(beadBrands))]
        realWorldBeads = realWorldBeads.reset_index(drop=True)
        #self.beadList = RGB_Distance(self.beadList, realWorldBeads)
        for bead in self.beadList:
            ### Get the RGB values of the given virtual bead
            virtualR = bead.color[0]
            virtualG = bead.color[1]
            virtualB = bead.color[2]

            smallestDistance = 1000 # Arbitrary starting value
            smallestRow = None # Index of row where smallest distance is observed
        
            for row in range(len(realWorldBeads["Color Name"])):
                ### Get the RGB values of the iterated physical bead
                physicalR = int(realWorldBeads["R"][row])
                physicalG = int(realWorldBeads["G"][row])
                physicalB = int(realWorldBeads["B"][row])

                ### Calculate the distance formula result for the virtual and physical beads
                currentDistance = math.dist([virtualR,virtualG,virtualB], [physicalR,physicalG,physicalB])

                if currentDistance < smallestDistance:
                    ### Set new smallestDistance
                    smallestDistance = currentDistance
                    smallestRow = row
                
                #print("FINISHED BEAD #" + str(bead.ID))
            
            ### Set bead attributes to those associated with the physical bead having the smallest distance
            newR = int(realWorldBeads["R"][smallestRow])
            newG = int(realWorldBeads["G"][smallestRow])
            newB = int(realWorldBeads["B"][smallestRow])
            bead.recolorBead(newR, newG, newB)
            bead.matchedColorName = realWorldBeads["Color Name"][smallestRow]
            bead.matchedColorBrand = realWorldBeads["Brand"][smallestRow]
            bead.matchedColorProductCode = realWorldBeads["Code"][smallestRow]


        try:
            successMessage = rainbowString.showMeTheColor("COMPLETED")
            print("matchColorscale() " + successMessage)
        except:
            print("matchColorscale() COMPLETED")

        



    def matchGrayscale(self, beadBrands):
        # Slice the realWorldBeads DataFrame such that only grayscale beads of the desired brand(s) remain        
        realWorldBeads = pd.read_excel("Real_World Bead Data.xlsx")
        realWorldBeads = realWorldBeads.loc[(realWorldBeads["Brand"].isin(beadBrands)) & (realWorldBeads["Color Scale"] == "Gray")]
        realWorldBeads = realWorldBeads.reset_index(drop=True)
        
        # For each Bead, loop through all the B channel values of the grayscale real-world beads
        # Only include the real-world beads which are made by the manufacturers identified in beadPattern.beadBrands
        for bead in self.beadList:    
            virtualB = bead.color[2]

            # Finds index (within realWorldBeads) of the real-world bead having the closest B value 
            index = (np.abs(realWorldBeads["B"] - virtualB)).argmin()
           
            matchedR = int(realWorldBeads["R"][index])        
            matchedG = int(realWorldBeads["G"][index])    
            matchedB = int(realWorldBeads["B"][index])    
            bead.recolorBead(matchedR, matchedG, matchedB)   

            bead.matchedColorName = realWorldBeads["Color Name"][index]
            bead.matchedColorBrand = realWorldBeads["Brand"][index]
            bead.matchedColorProductCode = realWorldBeads["Code"][index]
        
        print("matchGrayscale() COMPLETED")
        

   

    def beadify(self, width, height, backgroundColor):
        ### For each Bead object, parse through each pixel in a square region of s=beadDiameter
        
        mode = "RGB"
        size = (width, height)
        self.outputImage = Image.new(mode, size, backgroundColor)

        for bead in self.beadList:
            xStart = bead.leftmost
            yStart = bead.topmost
            xCurrent = xStart
            yCurrent = yStart
            xFinal = xStart + self.beadDiameter
            yFinal = yStart + self.beadDiameter

            beadOuterRadius = self.beadDiameter / 2
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
                        self.outputImage.putpixel((xCurrent, yCurrent), bead.color)
                    else:
                        # Set the parsed pixel as backgroundColor
                        self.outputImage.putpixel((xCurrent, yCurrent), backgroundColor)

                    yCurrent = yCurrent + 1
                
                xCurrent = xCurrent + 1    
            
        print("beadify() COMPLETED")



    