import matplotlib.pyplot as plt         # Only needed to excecute tests

import numpy as np
import pandas as pd
from collections import defaultdict     # Important for the union find algorithm
import cc3d                             # Library for 4-neighbour components



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ConnectedComponents(pairs):
    """ Using the union-find algorithm, this functions takes a set of general tuples
    and returns a list of general tuples with all the related elements """

    parent = {}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for t in pairs:
        if not t: continue
        first = t[0]
        if first not in parent: parent[first] = first
        for x in t[1:]:
            if x not in parent: parent[x] = x
            union(first, x)

    groups = defaultdict(list)
    for x in parent:
        groups[find(x)].append(x)
        
    # Sort for deterministic output (optional)
    return [tuple(sorted(g)) for g in groups.values()]

#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def CalculateAdjacentPairs(matrix, ID):
    """ Finds the perimeter of a cluster """
    matrix = matrix == ID                   # Mask all data other than the ID

    horizontal = np.sum(matrix[:, :-1] * matrix[:, 1:])
    vertical = np.sum(matrix[:-1, :] * matrix[1:, :])

    return horizontal + vertical

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
    adjacent_pairs = [CalculateAdjacentPairs(labels, ID) for ID in IDs]

    # Create a pandas data-frame with the data
    return pd.DataFrame({
        "ID": IDs.astype(int),
        "area": area.astype(int),
        "adjacent_pairs": adjacent_pairs,
    }).set_index("ID").drop(0) 
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ExtractBorders(labels):
    """ Extracts the borders of the clustered data: top, right, bottom, left """
    return labels[0, :], labels[:, -1], labels[-1, :], labels[:, 0]
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def BordersCheck(border1, border2):
    """ Takes 2 borders (numpy arrays) and returns a list of tuples with the IDs that collide with each other """
    # Pretty straightforward no need to explain
    mask = (border1 != 0) & (border2 != 0)
    pairs = list(zip(border1[mask], border2[mask]))

    # Here I group the different 2D tuples to general tuples with all the related clusters
    return ConnectedComponents(pairs)
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def MergeBordersData(chunk_data, merges, grid = False):
    """ Takes the dataframe of all data and operates its' rows according to the relations found during the border check. 

        INPUTS:
        -> chunk_data: DataFrame with rows area and adjacent_pairs. The index correspond to the cluster number ID.
        -> merges: set of tuples with integers (IDs of the chunk_data DataFrame). Every tuple indicates all the IDs are related

        RETURNS: Nothing, it just modifies the chunk_data DataFrame
    """
    
    # We'll iterate over each relation group
    for group in merges:
        
        group = np.asarray(group, dtype=int) 
        new_ID = np.max(group)  # The new ID of the whole group will be the max ID of it 
        
        # Sum up the rows
        merged_row = chunk_data.loc[group].sum(numeric_only=True)
        merged_row["ID"] = new_ID 

        chunk_data = chunk_data.drop(group)
        chunk_data.loc[new_ID] = merged_row


        # For visualization: make the original 2D grid change it's labels
        if type(grid) != bool:
            grid[np.isin(grid, group)] = new_ID

    
    return chunk_data 


#-------------------------------------------------------------------------------------------------------------------------------------------------------



#_______________________________________________________________________________________________________________________________________________________
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ChunkAnalysis(chunk, max_ID, save_map = False):
    """ This function will take a chunk 2D numpy array, and process it. 
        
        INPUTS:
        -> chunk: the binary 2D numpy array
        -> max_ID: the current max ID of the clusters, so every chunk has different IDs

        RETURNS:
        -> A Pandas dataframe with the geometrical data
        -> A list of lists of lists of the borders of the chunk (top, right, bottom, left)
        -> The max_ID of the cluster for the given chunk
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
    
    return chunk_data, borders, max_ID
#_______________________________________________________________________________________________________________________________________________________
#-------------------------------------------------------------------------------------------------------------------------------------------------------
            





# ==========================
#   MAIN TEST EXECUTION
# ==========================

if __name__ == "__main__":
    
    # HACK: this is probably gonna be stolen for the main script
    N = 15
    chunk_size = 15

    p = 0.35                                        
    data = np.random.binomial(1, 1-p, size=(N, 3*N))

    chunk_data_list = list()
    borders_list = list()
    max_ID = 0

    for s in range(0, 3*N, chunk_size):
        # WARNING: idk but it feels weird I have to do this to itterate over a __ horizontal array
        temp_data, temp_borders, temp_ID = ChunkAnalysis(CreateChunk(data, (0, s), chunk_size), max_ID, True)

        max_ID += temp_ID
        chunk_data_list.append(temp_data)
        borders_list.append(temp_borders)

    
    matches_list = list()
    
    # Relate the borders
    # TODO: this is kinda important: propose the algorithm to select the borders
    matches_list.extend(BordersCheck(borders_list[0][1], borders_list[1][3]))
    matches_list.extend(BordersCheck(borders_list[1][1], borders_list[2][3]))
    matches_list = ConnectedComponents(matches_list)                            # Merge all the data of all the borders
    print(matches_list)

    # Merge the chunks dataframes
    merged_data = pd.concat(chunk_data_list, ignore_index=False)
    del chunk_data_list # Free space
   



    print("-"*30, "\n")
    print("DATAFRAME BEFORE")
    print(merged_data)
    print("\n", "-"*30)

    plt.imshow(data)
    plt.title("before merging")
    plt.show()



    # Change the data according to the borders data
    merged_data = MergeBordersData(merged_data, matches_list, data)

    print("-"*30, "\n")
    print("DATAFRAME AFTER")
    print(merged_data)
    print("\n", "-"*30)

    plt.imshow(data)
    plt.title("after merging")
    plt.show()

