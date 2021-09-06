# Beautiful-Beadifier
Visualizes an input image as a large set of fuse beads (e.g., Perler Beads) for home decor. This program matches the colors found in the input image and matches them to the most similar real-world fuse bead product.

The inspiration for this project [comes from here!](https://www.reddit.com/r/nextfuckinglevel/comments/jas2w4/how_op_made_leonardo_dicaprio/)

## Outputs
The Beautiful Beadifier will save and open three outputs:
1. **A "beadified" image.** Your input image in bead form! This is what your final product will look like when you hang it up on your wall. This file will always be saved as a .jpg. [See beadified Gary.]() 
2. **A bead map.** An Excel file which uses cells. Cells are color-filled to depict the beadified image, and each cell contains the color name, brand, and product code of its corresponding beads. [See bead map of Gary.]()
3. **A bead counter.** An Excel file which details the number of each bead color required to . Use this as your shopping list when buying beads and pegboards! [See snippet of bead counter for Gary.]() 

## Use and Controls
`sourceFilename_` The location of the input image. The accepted file types are .jpg, .jpeg, and .png.
`beadDiameter_` The size of the virtual beads (in units of pixels). A smaller bead results in higher resolution but longer runtime.
`colorscaleOutput_` The selected color scheme for the beadified image. Set to `True` for an image in color; set to `False` for an image in grayscale.
`beadColorMatch_` 
`transparentToColor_`
`backgroundColor_`
`beadBrands_`
`pegboardDimensions_`

## Libraries to Import
These non-standard libraries must be imported to run the Beautiful Beadifier:
- Counter
- Openpyxl
- Pillow

