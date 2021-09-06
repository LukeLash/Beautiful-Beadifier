import math

def RGB_Distance(beadList, physicalBeads):
    for bead in beadList:
        ### Get the RGB values of the given virtual bead
        virtualR = bead.color[0]
        virtualG = bead.color[1]
        virtualB = bead.color[2]

        smallestDistance = 1000 # Arbitrary starting value
        smallestRow = None # Index of row where smallest distance is observed
    
        for row in range(len(physicalBeads["Color Name"])):
            ### Get the RGB values of the iterated physical bead
            physicalR = int(physicalBeads["R"][row])
            physicalG = int(physicalBeads["G"][row])
            physicalB = int(physicalBeads["B"][row])

            ### Calculate the distance formula result for the virtual and physical beads
            currentDistance = math.dist([virtualR,virtualG,virtualB], [physicalR,physicalG,physicalB])

            if currentDistance < smallestDistance:
                ### Set new smallestDistance
                smallestDistance = currentDistance
                smallestRow = row
            
            #print("FINISHED BEAD #" + str(bead.ID))
        
        ### Set bead attributes to those associated with the physical bead having the smallest distance
        newR = int(physicalBeads["R"][smallestRow])
        newG = int(physicalBeads["G"][smallestRow])
        newB = int(physicalBeads["B"][smallestRow])
        bead.recolorBead(newR, newG, newB)
        bead.matchedColorName = physicalBeads["Color Name"][smallestRow]
        bead.matchedColorBrand = physicalBeads["Brand"][smallestRow]
        bead.matchedColorProductCode = physicalBeads["Code"][smallestRow]


    return beadList

