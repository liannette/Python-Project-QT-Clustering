  #!/usr/bin/env python3


###############################################
# 22110 Python and Unix for Bioinformaticians #
#             Project 9: Functions            #
#                                             #
############################################### 


cluster_limit = 1



import sys, math, re

def calculate_distance(x, y):
    """ Calculates the distance between two data points"""
    sum_of_squares = 0
    for pos in range(len(x))[1:]:
        sum_of_squares += (float(x[pos]) - float(y[pos]))**2		# ValueError possible
    distance = math.sqrt(sum_of_squares)
    return distance



# Get file name and maximum diameter
if len(sys.argv) == 1:
    filename_in = input("Enter filename: ")
    max_diameter = input("Enter maximum cluster diameter: ")
elif len(sys.argv) == 3: 
    filename = sys.argv[1]
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
    # Saving the datapoints in a list of lists
    datapoints = list()
    infile = open(filename_in, 'r')					# IOError possible
    for line in infile:
        datapoints.append(line.split())
    infile.close()
    
    # Creating a dict of dict of all distances between any 2 points
    globalmax_distance = 0
    distances = dict()
    for point1 in datapoints:
        distances[point1[0]] = dict()
        for point2 in datapoints:
            distance = calculate_distance(point1, point2)  		# ValueError possible
            distances[point1[0]][point2[0]] = distance
            if distance > globalmax_distance:
                globalmax_distance = distance
    
    # Getting global maximum diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * globalmax_distance
    else: 
        max_diameter = float(max_diameter)

except IOError as error:
    sys.stderr.write("File I/O error, reason: " + str(error) + "\n")
    sys.exit(1)
except ValueError as error:
    print(str(error))
    sys.exit(1)
    
   

def candidate_point(datapoints, clusterpoints, max_diameter):
    """ Finds the next point for a cluster"""
    candidate_point = None
    new_diameter = max_diameter
    for datapoint in datapoints:
        max_dist = 0									# Maximum distance between the datapoint and any clusterpoint
        if datapoint not in clusterpoints:						# Set would be better
            # Find the clusterpoint with the biggest distance to the datapoint
            for clusterpoint in clusterpoints:
                dist = distances[datapoint[0]][clusterpoint[0]] 
                if dist > max_dist:
                    max_dist = dist
            if max_dist < new_diameter:
                # Set as datapoint potential candidate point
                new_diameter = max_dist
                candidate_point = datapoint
    if candidate_point != None:
        return candidate_point, new_diameter


def candidate_cluster(startpoint, datapoints, max_diameter, cluster_limit):
    """ Creates a candidate cluster"""
    cand_diameter = 0
    cand_cluster = list()
    cand_cluster.append(startpoint)
    cand_point = candidate_point(datapoints, cand_cluster, max_diameter)
    while cand_point is not None:
        cand_cluster.append(cand_point[0])
        cand_diameter = cand_point[1]
        cand_point = candidate_point(datapoints, cand_cluster, max_diameter)
    if cand_cluster >= cluster_limit:
        return cand_cluster, cand_diameter


def best_candidate_cluster(datapoints, max_diameter, cluster_limit):
    """ Finds the best cluster """
    best_cand_cluster = list([], max_diameter)
    for startpoint in datapoints:
        cand_cluster = candidate_cluster(startpoint, datapoints, max_diameter, cluster_limit)
        if candidate_cluster is not None:
            if len(cand_cluster[0]) is > len(best_cand_cluster[0]):
                best_cand_cluster = cand_cluster
            elif len(cand_cluster[0]) is == len(best_cand_cluster[0]):
                if cand_cluster[1] < best_cand_cluster[1]:
                    best_cand_cluster = cand_cluster
        return best_cand_cluster
      
      
def remove_datapoints(datapoints, best_candidate_cluster):
    i = 0
    while i < len(datapoints):   
        if datapoints[i] in best_candidate_cluster:
            del datapoints[i]
        else:
            i += 1



try: 
    filename_out = 'result-' + filename_in
    outfile = open(filename_out, 'w')
except IOError as error:
    sys.stderr.write("File I/O error, reason: " + str(error) + "\n")
    sys.exit(1)    


cluster_name = 1
best_cand_cluster = best_candidate_cluster(datapoints, max_diameter, cluster_limit)
    while best_cand_cluster is not None:
        # Print cluster to output file
        print('Cluster-'+str(cluster_name), file=outfile)
        for point in best_cand_cluster:
            print("\t".join(point), file=outfile)
        i += 1
        # remove cluster points from dataset
        remove_datapoints(datapoints, best_cand_cluster)
        # Get next cluster
        best_cand_cluster = best_candidate_cluster(datapoints, max_diameter, cluster_limit)
outfile.close()

    










