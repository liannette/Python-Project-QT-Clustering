  #!/usr/bin/env python3


#####################################################
#    22110 Python and Unix for Bioinformaticians    #
#             Project 9: QT Clustering              #
#        Annette Lien & Carlota Carbajo Moral       #
##################################################### 


# Minimum cluster size
cluster_limit = 1

import sys, math, re


#### Functions ####

def euclidean_distance(point1, point2):
    """ Calculates the euclidean distance between two data points"""
    sum_of_squares = 0
    for i in range(len(point1))[1:]:
        sum_of_squares += (float(point1[i]) - float(point2[i]))**2		# ValueError possible
    distance = math.sqrt(sum_of_squares)
    return distance
    
def candidate_point(datapoints_i, cluster_i, max_diameter):
    """ Finds the next point for a cluster"""
    point_i = None
    diameter = max_diameter
    for datapoint_i in datapoints_i.difference(cluster_i):
        max_dist = 0
        # Find the biggest distance between the datapoint and any clusterpoint
        for clusterpoint_i in cluster_i:
            if clusterpoint_i > datapoint_i:
                row, column = clusterpoint_i, datapoint_i
            else:
                row, column = datapoint_i, clusterpoint_i
            dist = distances[row][column] 
            if dist > max_dist:
                max_dist = dist
        if max_dist < diameter:
            # Set datapoint as potential candidate point
            diameter = max_dist
            point_i = datapoint_i
    return point_i, diameter

def candidate_cluster(startpoint_i, datapoints_i, max_diameter, cluster_limit):
    """ Creates a candidate cluster"""
    diameter = 0
    cluster_i = set()
    cluster_i.add(startpoint_i)
    point_i = candidate_point(datapoints_i, cluster_i, max_diameter)
    while point_i[0] is not None:
        cluster_i.add(point_i[0])
        diameter = point_i[1]
        point_i = candidate_point(datapoints_i, cluster_i, max_diameter)
    # Only return the cluster, if is contains enough points
    if len(cluster_i) >= cluster_limit:
        return cluster_i, diameter


def best_cluster(datapoints_i, max_diameter, cluster_limit):
    """ Finds the best cluster for a list of datapoints"""
    best_cand_cluster_i = set()
    diameter = max_diameter
    for startpoint_i in datapoints_i:
        cand_cluster_i = candidate_cluster(startpoint_i, datapoints_i, max_diameter, cluster_limit)
        if cand_cluster_i is not None:
            if len(cand_cluster_i[0]) > len(best_cand_cluster_i):
                best_cand_cluster_i = cand_cluster_i[0]
                diameter = cand_cluster_i[1]
            elif len(cand_cluster_i[0]) == len(best_cand_cluster_i) and cand_cluster_i[1] < diameter:
                best_cand_cluster_i = cand_cluster_i[0]
                diameter = cand_cluster_i[1]
    return best_cand_cluster_i



#### Main program ####

# Get file name and maximum diameter
if len(sys.argv) == 1:
    filename_in = input("Enter filename: ")
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
    
    # Initialize
    datapoints, distances, vector_size, globalmax_distance = list(), list(), None, 0
    
    # Go through file line by line
    infile = open(filename_in, 'r')								# IOError possible
    for line in infile:
        # Get datapoint
        new_point = list(line.split())
        # Assert that vector size is consistent
        if vector_size == None:
            vector_size = len(new_point)-1	   
        assert len(new_point)-1 == vector_size, 'Error: Every line has to represent a vector with format "<name> <number> <number> <number> ...". Vector size needs to be consistent.'
        # Calculate the distances to all previous points
        new_distances = list()
        for datapoint in datapoints:
            distance = euclidean_distance(datapoint, new_point)					# ValueError possible
            new_distances.append(distance)
            # Find the biggest distance
            if distance > globalmax_distance:
                globalmax_distance = distance
        distances.append(new_distances)
	# Add datapoint to tuple
        datapoints.append(new_point)
    # List of all datapoint indexes
    datapoints_i = set(range(len(datapoints)))
    infile.close()    
    
    
    # Getting maximum cluster diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * globalmax_distance
    else: 
        max_diameter = float(max_diameter)
    
    # Pepare outfile
    filename_out = 'result-' + filename_in
    outfile = open(filename_out, 'w')

    # Printing one cluster after another to the outfile
    cluster_count = 1
    cluster_i = best_cluster(datapoints_i, max_diameter, cluster_limit)
    while len(cluster_i) > 0:
        # Print cluster to output file
        print('-> Cluster', cluster_count, file=outfile)
        for point_i in sorted(cluster_i):
            point = datapoints[point_i]
            print("\t".join(point), file=outfile)
        # removing cluster points from dataset
        datapoints_i = datapoints_i.difference(cluster_i)
        # Get next cluster
        cluster_count += 1
        cluster_i = best_cluster(datapoints_i, max_diameter, cluster_limit)
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
    










