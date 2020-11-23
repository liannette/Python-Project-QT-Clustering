  #!/usr/bin/env python3


#####################################################
#    22110 Python and Unix for Bioinformaticians    #
#             Project 9: QT Clustering              #
#        Annette Lien & Carlota Carbajo Moral       #
##################################################### 


# Minimum cluster size
cluster_limit = 1

import sys, math, re


### Functions ###

def euclidean_distance(point1, point2):
    """ Calculates the euclidean distance between two data points"""
    sum_of_squares = 0
    for i in range(len(point1))[1:]:
        sum_of_squares += (float(point1[i]) - float(point2[i]))**2		# ValueError possible
    distance = math.sqrt(sum_of_squares)
    return distance

def add_distances(new_point, distances):
    """ Calculates distances to all previous points and adds it to the distances matrix """
    new_distances = list()
    for datapoint in datapoints:
        distance = euclidean_distance(datapoint, new_point)					# ValueError possible
        new_distances.append(distance)
    for i in range(len(new_distances[:-1])):
        distances[i].append(new_distances[i])
    distances.append(new_distances)
    
def candidate_point(datapoints_i, cluster_i, max_diameter, last_added_point_i, max_distances):
    """ Finds the next point for a cluster"""
    # Check all points that are not in a cluster or in this candidate cluster
    for datapoint_i in datapoints_i.difference(cluster_i):
        new_distance = distances[datapoint_i][last_added_point_i]
        if datapoint_i not in max_distances or max_distances[datapoint_i] < new_distance:
            max_distances[datapoint_i] = new_distance
    if max_distances != dict():
        # Get datapoint with the smallest value
        closest_point = sorted(max_distances.keys(), key=max_distances.get)[0]
        # Only return datapoint, if the new diameter is in the diameter limit
        if max_distances[closest_point] < max_diameter:
            return closest_point, max_distances[closest_point]

def candidate_cluster(startpoint_i, datapoints_i, max_diameter, cluster_limit):
    """ Creates a candidate cluster"""
    cluster_i = {startpoint_i}
    diameter = 0
    max_distances = dict()	# max distances between the datapoints to the cluster
    point_i = candidate_point(datapoints_i, cluster_i, max_diameter, startpoint_i, max_distances)
    while point_i is not None:
        cluster_i.add(point_i[0])
        del max_distances[point_i[0]]
        diameter = point_i[1]
        point_i = candidate_point(datapoints_i, cluster_i, max_diameter, point_i[0], max_distances)
    # Only return the cluster, if is contains enough points
    if len(cluster_i) >= cluster_limit:
        return cluster_i, diameter


def best_cluster(datapoints_i, max_diameter, cluster_limit):
    """ Finds the best cluster for a list of datapoints"""
    all_candidate_cluster = list()
    for startpoint_i in datapoints_i:
        candidate = candidate_cluster(startpoint_i, datapoints_i, max_diameter, cluster_limit)
        if candidate is not None:
            all_candidate_cluster.append(candidate) 
    if all_candidate_cluster != list():
        all_candidate_cluster.sort(key=lambda x: [len(x[0]), -x[1]], reverse= True)
        cluster_i = all_candidate_cluster[0][0]
        return cluster_i


### Main program ###


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
    datapoints, distances, columns = list(), list(), None
    
    infile = open(filename_in, 'r')					# IOError possible							
    for line in infile:
        # Get datapoint
        new_point = line.split()
        datapoints.append(new_point)
        # Assert that column number is consistent
        if columns == None:
            columns = len(new_point)   	   
        assert len(new_point) == columns, 'Error: Every line has to represent a vector with format "<name> <number> <number> <number> ...". Vector size needs to be consistent.'        
        # Calculate distances to all previous points and add to distances matrix
        add_distances(new_point, distances)
    infile.close() 
   
    # List of all datapoint indexes
    datapoints_i = set(range(len(datapoints)))

    # Getting maximum cluster diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * max([x for row in distances for x in row])
    else: 
        max_diameter = float(max_diameter)
    

    filename_out = 'result-' + filename_in
    outfile = open(filename_out, 'w')
    # Printing one cluster after another to the outfile
    cluster_count = 1
    cluster_i = best_cluster(datapoints_i, max_diameter, cluster_limit)
    while cluster_i != None:
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
    









