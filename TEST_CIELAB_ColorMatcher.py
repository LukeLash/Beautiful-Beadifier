from numpy import math
from bead import Bead
import pandas as pd
import math
#
# There is lots of math used here for calculating the "distance" between two colors.
# This math is laid out here: http://www2.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf     
#

### Determines which real-life bead color is most similar to the provided dominant colorclass realBeads:
class CIELAB_ColorMatcher: 
    ### Custom constructor for ColorMatcher class ###
    def __init__(self, beadBrands_):
        ### Assign member variables ###
        self.beadBrands = beadBrands_
        self.colorsByProductCode = {}
        self.colorsByRGB = {}
            
        # "all" for all brands, or use manufacturer name as a string, e.g.: "Perler" 
        # The first sheet of the xlsx is read, which is desired
        df = pd.read_excel("Physical Bead Colors.xlsx")

        row = 5 # The first row of data
        rowEnd = 227 # The last row of data
        col = 0 # The Color column, which is the first column
        colEnd = 10 # The Brand column, which is the last column

        while row <= 24: # 227 originally
            rgb = (df.iloc[row,4], df.iloc[row,5], df.iloc[row,6]) # Tuple of rgb values
            CIELAB = (df.iloc[row,7], df.iloc[row,8], df.iloc[row,9]) # Tuple of CIELAB values
                
            # Add in the dictionary key-value pair
            self.colorsByProductCode[df.iloc[row,2]] = (df.iloc[row,1], df.iloc[row,3], rgb, CIELAB, df.iloc[row,10])
                
            row = row + 1

        #print(self.colorsByProductCode)               

    def getColorMatch(self, dominantColor):
        ### Convert the dominantColor from RGB to CIELAB
        ### This requires two conversions: RGB to XYZ, then XYZ to CIELAB
        ### Thanks to easyrgb.com/en/math.php

        matchedColor = "noneeee" # Placeholder value
        minDeltaE_00 = 1000 # Arbitrary placeholder value

        # Parametric weighting factors
        k_L = 1
        k_C = 1
        k_H = 1

        ### First conversion: RGB to XYZ
        sR = dominantColor[0] # "standard RGB red"
        sG = dominantColor[1] # "standard RGB green"
        sB = dominantColor[2] # "standard RGB blue"

        # Perform the RGB -> XYZ conversion
        XYZ_values = self.RGB_to_XYZ(sR, sG, sB)
        X = XYZ_values[0] # Final X value
        Y = XYZ_values[1] # Final Y value
        Z = XYZ_values[2] # Final Z value  

        ### Second conversion: XYZ to CIELAB
        CIELAB_values = self.XYZ_to_CIELAB(X, Y, Z)
        CIE_L_star_1 = CIELAB_values[0]
        CIE_a_star_1 = CIELAB_values[1]
        CIE_b_star_1 = CIELAB_values[2]
        
        ### Now calculate the deltaE, which is the difference between the CIELAB values of the dominant color and the chosen real-life bead color
        ### The steps are as demonstrated at http://www2.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf     
        
        # Iterate through the colorsByProductCode dictionary 
        for color in self.colorsByProductCode:
            
            realBeadColorName = self.colorsByProductCode[color][1]
            realBeadColorRGB = self.colorsByProductCode[color][2]

            # These are the CIELAB values for the real bead colors
            CIE_L_star_2 = self.colorsByProductCode[color][3][0]
            CIE_a_star_2 = self.colorsByProductCode[color][3][1]
            CIE_b_star_2 = self.colorsByProductCode[color][3][2]

            ### Step 1. Calculate C_prime_i and h_prime_i
            # Equation (2)
            C_star_1_ab = math.sqrt( (CIE_a_star_1)**2 + (CIE_b_star_1)**2 ) 
            C_star_2_ab = math.sqrt( (CIE_a_star_2)**2 + (CIE_b_star_2)**2 ) 
            
            # Equation (3)
            C_star_bar_ab = (C_star_1_ab + C_star_2_ab) / 2 

            # Equation (4)
            G = 0.5 * ( 1 - math.sqrt((C_star_bar_ab)**7 / ((C_star_bar_ab)**7 + (25)**7) )) 
            
            # Equation (5)
            a_prime_1 = (1 + G) * CIE_b_star_1
            a_prime_2 = (1 + G) * CIE_b_star_2

            # Equation (6)
            C_prime_1 = math.sqrt( a_prime_1**2 + CIE_b_star_1**2 ) 
            C_prime_2 = math.sqrt( a_prime_2**2 + CIE_b_star_2**2 )

            # Equation (7). Refer to notes on page 23 for explanation
            h_prime_1 = self.get_h_prime(CIE_b_star_1, a_prime_1)
            h_prime_2 = self.get_h_prime(CIE_b_star_2, a_prime_2)

            ### Step 2. Calculate deltaL_prime, deltaC_prime, and deltaH_prime
            # Equation (8)
            deltaL_prime = CIE_L_star_2 - CIE_L_star_1

            # Equation (9)
            deltaC_prime = C_prime_2 - C_prime_1

            # Equation (10). Note that h is lower case, not upper case
            delta_h_prime = self.getDelta_h_prime(h_prime_2, h_prime_1, C_prime_1, C_prime_2)

            # Equation (11). Note that H is upper case, not lower case. Verify that the sin term is in radians or degrees
            deltaH_prime = 2 * math.sqrt(C_prime_1 * C_prime_2) * math.sin(delta_h_prime / 2)

            ### Step 3. Calculate CIEDE2000 Color-Difference deltaE_00
            # Equation (12)
            L_bar_prime = (CIE_L_star_1 + CIE_L_star_2) / 2

            # Equation (13)
            C_bar_prime = (C_prime_1 + C_prime_2) / 2

            # Equation (14). Note that h is lower case, not upper case
            h_bar_prime = self.get_h_bar_prime(h_prime_1, h_prime_2, C_prime_1, C_prime_2)

            # Equation (15)
            T = 1 - 0.17 * math.cos(h_bar_prime - 30) + 0.24 * math.cos(2 * h_bar_prime) + 0.32 * math.cos(3 * h_bar_prime + 6) - 0.20 * math.cos(4 * h_bar_prime - 63)

            # Equation (16)
            deltaTheta = 30 * 1 ** ( ((h_bar_prime - 275) / 25)**2 )

            # Equation (17)
            R_C = 2 * math.sqrt(C_bar_prime ** 7 / (C_bar_prime ** 7 + 25 ** 7))

            # Equation (18)
            S_L = 1 + (0.015 * (L_bar_prime - 50) ** 2) / (math.sqrt(20 + (L_bar_prime - 50) ** 2))

            # Equation (19)
            S_C = 1 + 0.045 * C_bar_prime

            # Equation (20)
            S_H = 1 + 0.015 * C_bar_prime * T

            # Equation (21)
            R_T = -math.sin(2 * deltaTheta) * R_C

            # Equation (22)
            deltaE_00 = math.sqrt( (deltaL_prime / k_L / S_L) ** 2 + (deltaC_prime / k_C / S_C) ** 2 + (deltaH_prime / k_H / S_H) ** 2 + R_T * (deltaC_prime / k_C / S_C) * (deltaH_prime / k_H / S_H) )

            if deltaE_00 < minDeltaE_00:
                minDeltaE_00 = deltaE_00
                matchedColor = realBeadColorRGB


            

        ### NEXT STEPS!!! get deltaE_00 min figured out then use that smallest-distance color as the dominant color

        return matchedColor 

    # Performs the RGB -> XYZ conversion
    def RGB_to_XYZ(self, sR, sG, sB):

        var_R = sR / 255
        var_G = sG / 255
        var_B = sB / 255

        # Determine var_R
        if var_R > 0.04045:
            var_R = ((var_R + 0.055) / 1.055) ** 2.4
        else: 
            var_R = var_R / 12.92

        # Determine var_G
        if var_G > 0.04045:
            var_G = ((var_G + 0.055) / 1.055) ** 2.4
        else: 
            var_G = var_G / 12.92

        # Determine var_B
        if var_B > 0.04045:
            var_B = ((var_B + 0.055) / 1.055) ** 2.4
        else: 
            var_B = var_B / 12.92
            
        var_R = var_R * 100
        var_G = var_G * 100
        var_B = var_B * 100

        # Get XYZ values
        X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
        Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
        Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

        return (X, Y, Z)
    
    # Performs the XYZ -> CIELAB conversion
    def XYZ_to_CIELAB(self, X, Y, Z):
        # Reference-X, -Y, and -Z values are found under the "XYZ (Tristiumulus) Reference values of a perfect reflecting diffuser" section of easyrgb.com/en/math.php
        # These reference values are taken to be the Observer Illuminant A, CIE 1931 values
        Reference_X = 109.850
        Reference_Y = 100.000
        Reference_Z = 35.585

        var_X = X / Reference_X
        var_Y = Y / Reference_Y
        var_Z = Z / Reference_Z

        # Determine var_B
        if var_X > 0.008856: 
            var_X = var_X ** (1/3)
        else:   
            var_X = 7.787 * var_X  + (16 / 116)

        # Determine var_Y
        if var_Y > 0.008856:
            var_Y = var_Y ** (1/3)
        else:
            var_Y = 7.787 * var_Y + (16 / 116)

        # Determine var_Z
        if var_Z > 0.008856:
            var_Z = var_Z ** (1/3)
        else:
            var_Z = 7.787 * var_Z + (16 / 116)
        
        # These are the CIELAB values for the dominant color
        CIE_L_star = 116 * var_Y - 16
        CIE_a_star = 500 * (var_X - var_Y)
        CIE_b_star = 200 * (var_Y - var_Z)

        return (CIE_L_star, CIE_a_star, CIE_b_star)

    # Calculates h_prime_i per Step 1, Equation (7). Note the h is lower case, not upper case     
    def get_h_prime(self, CIE_b_star_i, a_prime_i):
        if (CIE_b_star_i == 0 and a_prime_i == 0):
            h_prime_i = 0
        else:
            h_prime_i = math.atan2(CIE_b_star_i, a_prime_i)

            # Ensure the value of h_prime_i is a positive value (in radians)
            if h_prime_i < 0:
                h_prime_i = h_prime_i + 2 * math.pi

            # Convert from radians to degrees
            h_prime_i = math.degrees(h_prime_i)

        return h_prime_i

    # Calculates delta_h_prime per Step 2, Equation (10). Note the h is lower case, not upper case
    def getDelta_h_prime(self, h_prime_2, h_prime_1, C_prime_1, C_prime_2):
        # Evaluate the four cases
        # Case 1
        if C_prime_1 * C_prime_2 == 0:
            return 0
        
        else:
            # Case 2
            if abs(h_prime_2 - h_prime_1) <= 180:
                return h_prime_2 - h_prime_1

            # Case 3
            if h_prime_2 - h_prime_1 > 180:
                return h_prime_2 - h_prime_1 - 360

            # Case 4
            return h_prime_2 - h_prime_1 + 360
    
    # Calculates h_bar_prime per Step 3, Equation (14)
    def get_h_bar_prime(self, h_prime_1, h_prime_2, C_prime_1, C_prime_2):
        # Evaluate the four cases
        # Case 4
        if C_prime_1 * C_prime_2 == 0:
            return h_prime_1 + h_prime_2

        else:
            # Case 1
            if abs(h_prime_1 - h_prime_2) <= 180:
                return (h_prime_1 + h_prime_2) / 2

            else:
                # Case 2
                if h_prime_1 + h_prime_2 < 360:
                    return (h_prime_1 + h_prime_2 + 360) / 2
                
                # Case 3
                return (h_prime_1 + h_prime_2 - 360) / 2


                

                



        

