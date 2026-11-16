import matplotlib.pyplot as plt         # Only needed to excecute tests

import numpy as np
import pandas as pd
import cc3d         # Library for 4-neighbour components


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def perimeter(matrix, ID):
    """ Finds the perimeter of a cluster """
    matrix = matrix == ID                   # Mask all data other than the ID

    # Count exposed edges in each direction
    p = 0

    p += np.sum(matrix[0, :])       # Top boundary
    p += np.sum(matrix[-1, :])      # Bottom boundary
    p += np.sum(matrix[:, 0])       # Left boundary
    p += np.sum(matrix[:, -1])     # Right boundary

    # Internal edges
    p += np.sum(matrix[1:, :] != matrix[:-1, :])  # Vertical
    p += np.sum(matrix[:, 1:] != matrix[:, :-1])  # Horizontal

    return p
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateChunk(data, initial_cord, chunk_size):
    """ This functions takes a 2D numpy array and returns 
        -> A 2D numpy array of the respective chunk of interest
    """
    return data[initial_cord[0]:initial_cord[0]+chunk_size, initial_cord[1]:initial_cord[1]+chunk_size]
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateChunkData(labels):
    """ Takes the cluster data of a chunk and returns a dictionary with the info of each cluster """
    
    # Count the # of pixels with a given value (clusters)
    IDs, area = np.unique(labels, return_counts=True)
    perimeters = [perimeter(labels, ID) for ID in IDs]

    # Create a pandas data-frame with the data
    return pd.DataFrame({
        "ID": IDs.astype(int),
        "area": area.astype(int),
        "perimeter": perimeters,
        "previous_label": None
    }).set_index("ID").drop(0) 
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ExtractBorders(labels):
    """ Extracts the borders of the clustered data: top, right, bottom, left """
    return labels[0, :], labels[:, -1], labels[-1, :], labels[:, 0]
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def BordersUnion(borders, chunks):
    """ Takes the borders and data structures and merges the cluster information of the borders together """

    # Save the shape: shall be Nx, Ny, 4, chunk_size
    Nx, Ny, _, _ = borders.shape

    for i in range(Nx):
        for j in range(Ny):
            return

#-------------------------------------------------------------------------------------------------------------------------------------------------------



#_______________________________________________________________________________________________________________________________________________________
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ChunkAnalysis(chunk, max_ID, save_map = False):
    """ This function will take a big 2D numpy array, and process it. Returns
        -> A dictionary with the statistical data
        #TODO: will have to add the big-chunk processing too, or maybe directly write to memory the results of the current chunk processing
    """

    # This borders list has indexes up, right, down, left
    borders_list = list()                               # I will initialize a list of borders for each one of the chunks divisions. 
    chunks_data_list = list()                           # List with the dicts of each chunk's clusters parameters


    #   ------  MAIN FUNCTION
    # Analyse the clusters
    labels = cc3d.connected_components(chunk, connectivity=4) 
    labels[labels != 0] += max_ID   # The background cluster is kept to 0

    max_ID = np.max(labels)      # Update the max ID value

    # Create the chunk data: area and perimeter per cluster; and borders
    chunk_data = CreateChunkData(labels)
    borders = ExtractBorders(labels)

    # If we want to visualize the clusters, then save them directly on top of our data
    if save_map:
        chunk[:, :] =  labels
    
    print(chunk_data)
    plt.imshow(chunk)
    plt.show()
    return chunk_data, borders, max_ID
#_______________________________________________________________________________________________________________________________________________________
#-------------------------------------------------------------------------------------------------------------------------------------------------------
            


    
N = 40
chunk_size = 20

p = 0.20                                        
data = np.random.binomial(1, 1-p, size=(N, N))

ChunkAnalysis(CreateChunk(data, (0, 0), chunk_size), 0, True)


