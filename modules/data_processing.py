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
    """ Takes the labels of a chunk and returns a dataframe with area and adjacent pairs per cluster """
    n = int(labels.max())

    area = np.bincount(labels.ravel(), minlength=n + 1)[1:]

    # Each pair counted once: right and down neighbours
    h = (labels[:, 1:] == labels[:, :-1]) & (labels[:, 1:] != 0)
    v = (labels[1:, :] == labels[:-1, :]) & (labels[1:, :] != 0)
    adjacent_pairs = (np.bincount(labels[:, 1:][h], minlength=n + 1)
                      + np.bincount(labels[1:, :][v], minlength=n + 1))[1:]

    return pd.DataFrame({
        "ID": np.arange(1, n + 1, dtype=np.int64),
        "area": area.astype(np.int64),
        "adjacent_pairs": adjacent_pairs.astype(np.int64),
    }).set_index("ID")
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ExtractBorders(labels):
    """ Extracts the borders of the clustered data: top, right, bottom, left """
    return labels[0, :], labels[:, -1], labels[-1, :], labels[:, 0]
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def BordersCheck(border1, border2):
    """ Takes 2 aligned borders (numpy arrays) and returns an array with rows (id_a, id_b, n_contacts) """
    mask = (border1 != 0) & (border2 != 0)

    pairs = np.stack((border1[mask], border2[mask]), axis=1).astype(np.int64)
    uniq, counts = np.unique(pairs, axis=0, return_counts=True)

    return np.column_stack((uniq, counts))          
#-------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------
def MergeBordersData(chunk_data, merges, seams, grid = False):
    """ Merges clusters according to the border relations and adds the seam contacts.

        INPUTS:
        -> chunk_data: DataFrame (index = global ID) with columns area and adjacent_pairs
        -> merges: list of tuples (output of ConnectedComponents), each one a group of related IDs
        -> seams: N x 3 array with rows (id_a, id_b, n_contacts), from all the BordersCheck calls

        RETURNS: DataFrame with one row per final cluster: area, adjacent_pairs, perimeter
    """

    # Every ID in a group maps to the max ID of the group
    mapping = {int(x): int(max(g)) for g in merges for x in g}

    def remap(ids):
        s = pd.Series(ids)
        return s.map(mapping).fillna(s).astype(np.int64).to_numpy()

    # Sum area and adjacent pairs of the pieces belonging to the same final cluster
    final_ids = remap(chunk_data.index.to_numpy())
    merged = chunk_data[["area", "adjacent_pairs"]].groupby(final_ids).sum()
    merged.index.name = "ID"

    # Add the contacts across the seams to the final clusters
    if len(seams) > 0:
        seam_adj = pd.Series(seams[:, 2]).groupby(remap(seams[:, 0])).sum()
        merged["adjacent_pairs"] = merged["adjacent_pairs"].add(seam_adj, fill_value=0).astype(np.int64)

    # For visualization: relabel the original 2D grid
    if type(grid) != bool:
        for group in merges:
            grid[np.isin(grid, group)] = max(group)

    # -- PERIMETER column
    merged["perimeter"] = 4 * merged["area"] - 2 * merged["adjacent_pairs"]

    return merged
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

    chunk_data = CreateChunkData(labels)            # local labels
    chunk_data.index = chunk_data.index + max_ID    # shift to global IDs

    labels = labels.astype(np.int64)                # avoid uint32 overflow with big offsets
    labels[labels != 0] += max_ID

    max_ID += len(chunk_data)                       # running total of clusters

    borders = ExtractBorders(labels)

    if save_map:
        chunk[:, :] = labels

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


    original = data.copy() 
    chunk_data_list = list()
    borders_list = list()
    max_ID = 0

    for s in range(0, 3*N, chunk_size):
        # WARNING: idk but it feels weird I have to do this to itterate over a __ horizontal array
        temp_data, temp_borders, temp_ID = ChunkAnalysis(CreateChunk(data, (0, s), chunk_size), max_ID, True)
        chunk_data_list.append(temp_data)
        borders_list.append(temp_borders)

        max_ID = temp_ID

    
    matches_list = list()
    
    # Relate the borders
    # TODO: this is kinda important: propose the algorithm to select the borders
    seams = np.concatenate([
        BordersCheck(borders_list[0][1], borders_list[1][3]),
        BordersCheck(borders_list[1][1], borders_list[2][3]),
    ])
    pairs = [tuple(p) for p in np.unique(seams[:, :2], axis=0).tolist()]
    matches_list = ConnectedComponents(pairs)                            # Merge all the data of all the borders
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
    merged_data = MergeBordersData(merged_data, matches_list, seams, data)

    print("-"*30, "\n")
    print("DATAFRAME AFTER")
    print(merged_data)
    print("\n", "-"*30)

    plt.imshow(data)
    plt.title("after merging")
    plt.show()

