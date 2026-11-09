"""
This script is in charge of the main execution of the project:

1. Process the real data (.tif) images
"""
import numpy as np
import matplotlib.pyplot as plt
import modules.data_processing as dp        # All needed functions to process the .tif images



"""
----------------------------------------
        READ THE DATA
Important to notice that we have 3 different types of data:
    1. 2000 cover: 0-100% cover per pixer on the year 2000
    2. Loss: 0-25, 0 indicating no loss, >0 indicating a loss of forest in that respective year
    3. Mask: [1,2], indicates wheter the pixel is land or water
"""

coordinates = "0N70W"

data = dp.read_coordinates(coordinates, 20, initial_cell = (0, 0), length = 4000)

print(data.shape)

plt.imshow(data)
plt.show()



