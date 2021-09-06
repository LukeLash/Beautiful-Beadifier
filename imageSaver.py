import os
from colorama import Fore, Style

def save(bP, sourceFilename, colorscaleOutput):
    """ Saves the output image
    """
        
    ### Save the output image. If a folder associated with the image title doesn't yet exist, a new folder is created.  
    outputTitle = sourceFilename[sourceFilename.find("/") + 1:sourceFilename.find(".")] # Get the title of outputImage
    
    if colorscaleOutput:
        filename = outputTitle + "_" + str(bP.totalBeads) + "_beads_IMAGE_COLOR" + ".jpg"
    else:
        filename = outputTitle + "_" + str(bP.totalBeads) + "_beads_IMAGE_GRAY" + ".jpg"

    if os.path.isdir("Outputs" + "/" + outputTitle + "/"):
        bP.outputImage.save("Outputs" + "/" + outputTitle + "/" + filename)
    else:
        os.makedirs("Outputs" + "/" + outputTitle + "/")
        bP.outputImage.save("Outputs" + "/" + outputTitle + "/" + filename)
    
    print(Fore.GREEN + "--------------------------------------------------")
    print("Output image SAVED" + Style.RESET_ALL)
