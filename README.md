# Beautiful-Beadifier
Visualizes an input image as a large set of [fuse beads](https://www.google.com/search?q=fuse+beads&rlz=1C1ONGR_enUS942US942&sxsrf=AOaemvKP31wq8HmeJDoNF0ePfcJvXuiCRQ:1630972309504&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjAr5WpxevyAhXSdd8KHZ6CCpcQ_AUoAnoECAEQBA&biw=1536&bih=722) (e.g., Perler Beads) for home decor. This program identifies the colors found in an input image and matches them to the most similar real-world fuse bead product.

The inspiration for this project [comes from here!](https://www.reddit.com/r/nextfuckinglevel/comments/jas2w4/how_op_made_leonardo_dicaprio/)

## Outputs
The Beautiful Beadifier will save and open three outputs:
1. **A "beadified" image.** Your input image in bead form! This is what your final product will look like when you hang it up on your wall. This file will always be saved as a .jpg. [See beadified Gary.](https://github.com/LukeLash/Beautiful-Beadifier/blob/main/Outputs/gary/gary_15360_beads_IMAGE_COLOR.jpg) 
2. **A bead map.** An Excel file whose cells have been color-filled to reflect the beadified image. Each cell contains the color name, brand, and product code of its corresponding beads. [See bead map of Gary.](https://github.com/LukeLash/Beautiful-Beadifier/blob/main/Outputs/gary/gary_15360_beads_MAP_COLOR.xlsx)
3. **A bead counter.** An Excel file which details the number of each bead color required to build your final product. The number of pegboards required is also specified. Use this as your shopping list when buying beads and pegboards! [See bead counter for Gary.](https://github.com/LukeLash/Beautiful-Beadifier/blob/main/Outputs/gary/gary_15360_beads_COUNTER_COLOR.xlsx) 

## Use and Controls
`sourceFilename_` The location of the input image. The accepted file types are .jpg, .jpeg, and .png.

`beadDiameter_` The size of the virtual beads (in units of pixels). A smaller bead results in higher resolution but longer runtime.

`colorscaleOutput_` Boolean indicating the selected color scheme for the beadified image. Set to `True` for an image in color; set to `False` for an image in grayscale.

`beadColorMatch_` Boolean indicating whether the color matching operation should be performed. Set to `True` to perform color matching. If set to `False`, color matching will not be performed and the outputs will reflect the original colors from the input image. ***Aside from testing, this value should always be set to*** `True`***.***

`transparentToColor_` An RGB tuple. Some input images (typically .png files) contain transparent pixels. These pixels are recolored to `transparentToColor_`.

`backgroundColor_` An RGB tuple representing the color displayed both between the beads and within the holes of the beads. The typical selection is `(0, 0, 0)` for a black background.

`beadBrands_` A list containing bead manufacturers whose beads are available for color matching. See the [Real_World Bead Data spreadsheet for available beads.](https://github.com/LukeLash/Beautiful-Beadifier/blob/main/Real_World%20Bead%20Data.xlsx). This list can be modified to permit color matching for one or more manufacturers.

`pegboardDimensions_` A tuple containing the width and height (in units of pegs) of a rectangular pegboard. For example, a pegboard [like this one](https://www.amazon.com/Boards-Square-Plastic-Pegboards-Suitable/dp/B087R9VQ51/ref=sr_1_9?crid=R1U6MYOFBCH2&dchild=1&keywords=fuse+bead+pegboard&qid=1630972923&sprefix=fuse+bead+peg%2Caps%2C178&sr=8-9) will have dimensions of `(29, 29)`. 

## Libraries to Import
These non-standard libraries must be imported to run the Beautiful Beadifier:
- Collections
- Colorama
- Matplotlib
- Numpy
- Openpyxl
- Pandas
- Pillow
