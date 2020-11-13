  #!/usr/bin/env python3


###############################################
# 22110 Python and Unix for Bioinformaticians #
#           Project 9: QT-Clustering          #
#                                             #
############################################### 


# Minimum cluster size
cluster_limit = 1

import sys, math, re


#### Functions ####

def calculate_distance(point1, point2):
    """ Calculates the distance between two data points"""
    sum_of_squares = 0
    for i in range(len(point1))[1:]:
        sum_of_squares += (float(point1[i]) - float(point2[i]))**2		# ValueError possible
    distance = math.sqrt(sum_of_squares)
    return distance
    
def candidate_point(datapoints, cluster, max_diameter):
    """ Finds the next point for a cluster"""
    point = None
    diameter = max_diameter
    for datapoint in datapoints:
        max_dist = 0									# Maximum distance between the datapoint and any clusterpoint
        if datapoint not in cluster:							# Set would be better
            # Find the clusterpoint with the biggest distance to the datapoint
            for clusterpoint in cluster:
                dist = distances[datapoint[0]][clusterpoint[0]] 
                if dist > max_dist:
                    max_dist = dist
            if max_dist < diameter:
                # Set as datapoint potential candidate point
                diameter = max_dist
                point = datapoint
    if point != None:
        return point, diameter

def candidate_cluster(startpoint, datapoints, max_diameter, cluster_limit):
    """ Creates a candidate cluster"""
    diameter = 0
    cluster = list()
    cluster.append(startpoint)
    point = candidate_point(datapoints, cluster, max_diameter)
    while point is not None:
        cluster.append(point[0])
        diameter = point[1]
        point = candidate_point(datapoints, cluster, max_diameter)
    if len(cluster) >= cluster_limit:
        return cluster, diameter

def best_cluster(datapoints, max_diameter, cluster_limit):
    """ Finds the best cluster for a list of datapoints"""
    best_cand_cluster = list()
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
    if best_cand_cluster != []:
        return best_cand_cluster
    
def remove_datapoints(datapoints, cluster):
    """ Removes the datapoints that have been added to a cluster """
    i = 0
    while i < len(datapoints):   
        if datapoints[i] in cluster:
            del datapoints[i]
        else:
            i += 1



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

# Check if maximum diameter makes sense
result = re.search(r'\d+(\.\d+)?%?', max_diameter)
while result == None:
    print('Error: Maximum cluster diameter must be a number or a percentage.')
    max_diameter = input("Enter maximum cluster diameter: ")
    result = re.search(r'\d+(\.\d+)?%?', max_diameter)

    
try:    
    # Saving the datapoints from the input file in a list of lists
    datapoints = list()
    infile = open(filename_in, 'r')					# IOError possible
    column_number = None
    for line in infile:
        point = line.split()
        if column_number == None:
            column_number = len(point)
        assert len(point) == column_number, 'Error: Every line has to represent a vector with the format "<name> <number> <number> <number> ...". Every vector needs to have the same size.'
        datapoints.append(point)
    infile.close()    
    
    # Creating a dict (of dicts) of all distances between any 2 points
    globalmax_distance = 0
    distances = dict()
    for point1 in datapoints:
        distances[point1[0]] = dict()
        for point2 in datapoints:
            distance = calculate_distance(point1, point2)  		# ValueError possible
            distances[point1[0]][point2[0]] = distance
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
    while cluster is not None:
        # Print cluster to output file
        print('--> Cluster-'+str(cluster_index), file=outfile)
        for point in cluster:
            print("\t".join(point), file=outfile)
        # removing cluster points from dataset
        remove_datapoints(datapoints, cluster)
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
    










