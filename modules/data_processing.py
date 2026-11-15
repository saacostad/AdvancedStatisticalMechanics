import numpy as np
import matplotlib.pyplot as plt 

import cc3d         # Library for 4-neighbour components


N = 100
chunk_size = 50

p = 0.20
data = np.random.binomial(1, 1-p, size=(N, N))



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



def CreateChunk(data, initial_cord, chunk_size):
    """ This functions takes a 2D numpy array and returns 
        -> A 2D numpy array of the respective chunk of interest
    """
    return data[initial_cord[0]:initial_cord[0]+chunk_size, initial_cord[1]:initial_cord[1]+chunk_size]



def CreateChunkData(labels):
    """ Takes the cluster data of a chunk and returns a dictionary with the info of each cluster """
    
    # Count the # of pixels with a given value (clusters)
    IDs, area = np.unique(labels, return_counts=True)
    perimeters = [perimeter(labels, ID) for ID in IDs]

    # Format the lists
    values = zip(area, perimeters)

    # Create the dict
    chunk_data = dict(zip(IDs, values))

    return chunk_data


def AnalysisBigData(data, chunk_size):
    """ This function will take a big 2D numpy array, and process it. Returns
        -> A dictionary with the statistical data
        #TODO: will have to add the big-chunk processing too, or maybe directly write to memory the results of the current chunk processing
    """

    size = data.shape[0]                    # size of the data (shall be squared because I'm too lazy for not-squary shit)
    N = int(size / chunk_size)              # How many partitions on one axis
    
    max_ID = 0                              # Global counter for the max cluster ID

    boders = list()                         # I will initialize a list of borders for each one of the chunks divisions. 
    chunks_data_list = list()                    # List with the dicts of each chunk's clusters parameters

    #   ------  MAIN LOOP
    # TODO: maybe, just maybe, I'll have to optimize this
    for j in range(0, size, chunk_size):

        horizontal_borders = list()             # Create a list to save the horizontal borders

        for i in range(0, size, chunk_size): 
            
            # Create the chunk
            chunk_extract = CreateChunk(data, (i, j), chunk_size)            

            # Analyse the clusters
            labels = cc3d.connected_components(chunk_extract, connectivity=4) + max_ID
            max_ID = np.max(labels)      # Update the max ID value

            # Create the chunk data: area and perimeter per cluster
            chunk_data = CreateChunkData(labels)



    



AnalysisBigData(data, 50)
