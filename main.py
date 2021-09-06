from beadPattern import BeadPattern
import math
import imageSaver
import beadMapSaver
import counterSaver
from colorama import Fore, Style
import os

def main():
    ### User defines these control variables
    sourceFilename_ = "SourceImages/handsome.jpg" # Location of image file
    beadDiameter_ = 8 # Bead size (in pixels). Smaller size yields higher resolution of beaded image
    colorscaleOutput_ = 1 # True -> color output image. False -> gray output image 
    beadColorMatch_ = 1 # If true, will provide names of matched bead colors
    transparentToColor_ = (255, 179, 71)
    backgroundColor_ = (0, 0, 0) # The color shown in the space between beads. Is also the color of the bore of the bead
    beadBrands_ = ["Artkal", "Perler"] # Bead manufacturers. May be used to specify certain bead manufacturers
    pegboardDimensions_ = (29, 29) # The width, height (in beads) of a physical pegboard

    ### Constructs the BeadPattern. Builds a list of Bead objects
    bP = BeadPattern(sourceFilename_, beadDiameter_, colorscaleOutput_, transparentToColor_, backgroundColor_, beadColorMatch_, beadBrands_)
    
    ### Calcuate the number of pegboards required to build the output image
    pegboardColumns = math.ceil(bP.beadColumns / pegboardDimensions_[0])
    pegboardRows = math.ceil(bP.beadRows / pegboardDimensions_[1]) 
    pegboardsRequired = pegboardRows * pegboardColumns

    ### Saves the output image and shows it.
    imageSaver.save(bP, sourceFilename_, colorscaleOutput_)
    bP.outputImage.show()

    ### Builds, saves and shows the bead map.
    mapFilePath = beadMapSaver.save(bP, sourceFilename_, colorscaleOutput_)
    os.system("start EXCEL.EXE " + mapFilePath)

    ### Builds, saves, and shows the bead counter.
    counterFilePath = counterSaver.save(bP, sourceFilename_, colorscaleOutput_, pegboardDimensions_, pegboardsRequired)
    os.system("start EXCEL.EXE " + counterFilePath)

    ### Prints out the useful metrics for building the real-world output image
    ### Each bead is 5 mm in diameter, or 0.0164042 feet
    widthInFeet = str(round(bP.beadColumns * 0.0164042, 2))
    heightInFeet = str(round(bP.beadRows * 0.0164042, 2))

    try:
        print(Fore.GREEN + "--------------------------------------------------")
        print("Total beads: " + str(bP.totalBeads) + " | Size: " + heightInFeet + " feet high and " + widthInFeet + " feet wide" + " | Pegboards required: " + str(pegboardsRequired))        
        print(Style.RESET_ALL)
    except:
        print("Total beads: " + str(bP.totalBeads) + " | Size: " + heightInFeet + " feet high and " + widthInFeet + " feet wide" + " | Pegboards required: " + str(pegboardsRequired))



if __name__ == "__main__":
    os.system('cls')
    main()