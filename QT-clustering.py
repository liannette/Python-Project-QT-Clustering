  #!/usr/bin/env python3


#####################################################
#    22110 Python and Unix for Bioinformaticians    #
#             Project 9: QT Clustering              #
#        Annette Lien & Carlota Carbajo Moral       #
##################################################### 

# TO DO:
# 1. Make a function to create the dict of the distances


# Minimum cluster size
cluster_limit = 1

import sys, math, re


#### Functions ####

def euclidean_distance(point1, point2):
    """ Calculates the euclidean distance between two data points"""
    sum_of_squares = 0
    # First element of point1 list is the name of the point
    for i in range(len(point1))[1:]:
        sum_of_squares += (float(point1[i]) - float(point2[i]))**2		# ValueError possible
    distance = math.sqrt(sum_of_squares)
    return distance
    
def candidate_point(datapoints, cluster, max_diameter):
    """ Finds the next point for a cluster"""
    point = None
    diameter = max_diameter
    # Check only the points in datapoints that are not in the cluster
    for datapoint in datapoints.difference(cluster):
        max_dist = 0
        # Find the biggest distance between the datapoint and any clusterpoint
        for clusterpoint in cluster:
            # Convert the elements of the sorted list (the smallest appears first) in a string
            key = ' '.join(sorted([datapoint[0],clusterpoint[0]]))
            dist = distances[key]
            # Select greatest distance between cluster points and the datapoint
            if dist > max_dist:
                max_dist = dist
        # Select the datapoint that is nearer to the cluster point (smallest diameter)
        if max_dist < diameter:
            # Set datapoint as potential candidate point
            diameter = max_dist
            point = datapoint
    return point, diameter

def candidate_cluster(startpoint, datapoints, max_diameter, cluster_limit):
    """ Creates a candidate cluster"""
    diameter = 0
    cluster = set()
    cluster.add(startpoint)
    point = candidate_point(datapoints, cluster, max_diameter)
    # point[0] will be None when there are no points with a distance between them smaller than the maximum cluster diameter
    while point[0] is not None:
        cluster.add(point[0])
        diameter = point[1]
        point = candidate_point(datapoints, cluster, max_diameter)
    if len(cluster) >= cluster_limit:
        return cluster, diameter


def best_cluster(datapoints, max_diameter, cluster_limit):
    """ Finds the best cluster for a list of datapoints"""
    best_cand_cluster = set()
    diameter = max_diameter
    for startpoint in datapoints:
        cand_cluster = candidate_cluster(startpoint, datapoints, max_diameter, cluster_limit)
        if cand_cluster is not None:
            if len(cand_cluster[0]) > len(best_cand_cluster):
                best_cand_cluster = cand_cluster[0]
                diameter = cand_cluster[1]
            elif len(cand_cluster[0]) == len(best_cand_cluster) and cand_cluster[1] < diameter:
                best_cand_cluster = cand_cluster[0]
                diameter = cand_cluster[1]
    return best_cand_cluster



#### Main program ####

# Get file name and maximum diameter
if len(sys.argv) == 1:
    filename_in = input("Enter filename: ")
    max_diameter = input("Enter maximum cluster diameter: ")
elif len(sys.argv) == 2:
    filename_in = sys.argv[1]
    max_diameter = input("Enter maximum cluster diameter: ")
elif len(sys.argv) == 3: 
    filename_in = sys.argv[1]
    max_diameter = sys.argv[2]
else:
    sys.stderr.write("Usage: QT-clustering.py <filename> <maximum cluster diameter>\n")
    sys.exit(1)


try:
    # Assert that maximum diameter makes sense
    result = re.search(r'\d+(\.\d+)?%?', max_diameter)
    assert result != None, 'Usage: QT-clustering.py <filename> <maximum cluster diameter>\nMaximum cluster diameter must be a number or a percentage.'
    
    # Saving the datapoints from the input file in a set of tuples
    datapoints = set()
    infile = open(filename_in, 'r')					# IOError possible
    vector_size = None
    for line in infile:
        point = tuple(line.split())
        datapoints.add(point)
        # Assert that vector size is consistent
        if vector_size == None:
            vector_size = len(point)-1
        assert len(point)-1 == vector_size, 'Error: Every line has to represent a vector with format "<name> <number> <number> <number> ...". Vector size needs to be consistent.'
    infile.close()    
    
    # Creating a dict of all distances between any 2 points
    globalmax_distance = 0
    distances = dict()
    for point1 in datapoints:
        for point2 in datapoints:
            key = ' '.join(sorted([point1[0],point2[0]]))
            if key not in distances:
                distance = euclidean_distance(point1, point2)  		# ValueError possible
                distances[key] = distance
                if distance > globalmax_distance:
                    globalmax_distance = distance
    
    # Getting maximum cluster diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * globalmax_distance
    else: 
        max_diameter = float(max_diameter)
    
    # Pepare outfile
    filename_out = 'result-' + filename_in
    outfile = open(filename_out, 'w')

    # Printing one cluster after another to the outfile
    cluster_index = 1
    cluster = best_cluster(datapoints, max_diameter, cluster_limit)
    while len(cluster) > 0:
        # Print cluster to output file
        print('-> Cluster', cluster_index, file=outfile)
        for point in sorted(cluster):
            print("\t".join(point), file=outfile)
        # removing cluster points from dataset
        datapoints = datapoints.difference(cluster)
        # Get next cluster
        cluster_index += 1
        cluster = best_cluster(datapoints, max_diameter, cluster_limit)
    outfile.close()
    

except IOError as error:
    print("Can't open file, reason: " + str(error))
    sys.exit(1)    	
except ValueError as error:
    print(str(error))
    sys.exit(1)
except AssertionError as error:
    print(str(error))
    sys.exit(1)
    










