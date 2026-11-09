import numpy as np
import tifffile as tf


def tiff_to_numpy(path, initial_cell, length):
    """ Read a path to a .tif image and returns a numpy array with it's data """
    data = tf.imread(path)

    if length == 0:
        return data 
    else:
        a = initial_cell[0]
        b = initial_cell[1]
        new_data = data[a:a+length, b:b+length].copy()
        del data                                        # To free space
        return new_data


def read_2000_data(path, initial_cell, length, treshold):
    """
    Reads the original year 2000 tree cover data [0-100%] and returns a binary map
    for wheter the pixel is forested or not given a treshold
    """
    data = tiff_to_numpy(path, initial_cell, length)                              # Read the data
    mask = (data > treshold).astype(int)                    # Create the binary mask

    return mask


def read_coordinates(coordinates, initial_cell = (0, 0), length = 0, treshold = 30):
    """ This function takes the coordinates (e.g. 0N70W) and reads the 3 files
        - 2000      -->  IMPORTANT: need to select a treshold to create the binary mask
        - loss
        - mask
    inside of the folder `data/{coordinates}/`

    It takes an initial coordinate (a, b) and a length L 
    to separate this data into chunks of size L [as these data can be too heavy for certain machines]

    If length = 0, it returns all
    """
    data_2000 = read_2000_data(f"data/{coordinates}/2000.tif", initial_cell, length, treshold) 
    data_loss = tiff_to_numpy(f"data/{coordinates}/loss.tif", initial_cell, length)
    data_mask = tiff_to_numpy(f"data/{coordinates}/mask.tif", initial_cell, length)

    return data_2000, data_loss, data_mask


