  #!/usr/bin/env python3


###############################################
# 22110 Python and Unix for Bioinformaticians #
#             Project 9: Functions            #
#                                             #
############################################### 



import sys, math, re

def calculate_distance(x, y):
    """ Calculates the distance between two data points"""
    sum_of_squares = 0
    for pos in range(len(x))[1:]:
        sum_of_squares += (float(x[pos]) - float(y[pos]))**2
    distance = math.sqrt(sum_of_squares)
    return distance

try:
    # Get file name and maximum diameter
    if len(sys.argv) == 1:
        filename = input("Enter filename: ")
        max_diameter = input("Enter maximum cluster diameter: ")
    elif len(sys.argv) == 3: 
        filename = sys.argv[1]
        max_diameter = sys.argv[2]		# ERROR possible
    else:
        sys.stderr.write("Usage: QT-clustering.py <filename> <maximum cluster diameter>\n")
        sys.exit(1)
    
    # Check if maximum diameter makes sense
    result = re.search(r'\d+(\.?\d*)%?', max_diameter)
    while result == None:
        print('Error: Maximum cluster diameter must be a number or a percentage.')
        max_diameter = input("Enter maximum cluster diameter: ")
        result = re.search(r'\d+(\.?\d*)%?', max_diameter)
    
    # Saving the datapoints in a list of lists
    datapoints = []
    infile = open(filename, 'r')
    for line in infile:
        datapoints.append(line.split())
    infile.close()
    
    # Creating a dict of dict of all distances between any 2 points
    globalmax_distance = 0
    distances = dict()
    for point1 in datapoints:
        distances[point1[0]] = dict()
        for point2 in datapoints:
            distance = calculate_distance(point1, point2)
            distances[point1[0]][point2[0]] = distance
            if distance > globalmax_distance:
                max_distance = distance
    
    # Getting global maximum diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * globalmax_distance
    else: 
        max_diameter = float(max_diameter)

except IOError as error:
    sys.stderr.write("File I/O error, reason: " + str(error) + "\n")
    sys.exit(1)
   

''' 
#print(distances[datapoints[0][0]])


cluster = list()
min_distance = max_distance

#Candidate clusters
def qt_clust(datapoints, max_diameter):
    output_cluster = list()
    for i in range(len(datapoints))[0]:
        cluster = list()
        cluster += datapoints[i]
        min_distance = max_distance
        flag = True
        while flag == True:
            for j in range(len(datapoints)):
                if datapoints[j] not in cluster:
                    distance = float(distances[datapoints[i]][datapoints[j]])
                    if distance < min_distance:
                        min_distance = distance
                        min_point = datapoints[j]
            if min_distance <= max_diameter:        
                cluster += min_point
            else: 
                flag = False   
        if len(output_cluster) < len(cluster):
            output_cluster = cluster
    if len(output_cluster) != 1:
        return output_cluster
'''

def candidate_point(datapoints, clusterpoints):
    """ """
    candidate_point = None
    min_dist = globalmax_distance
    for datapoint in datapoints:
        max_dist = 0						# Maximum distance between the datapoint and any clusterpoint
        if datapoint not in clusterpoints:			# Set would be better
            for clusterpoint in clusterpoints:
                dist = distances[datapoint[0]][clusterpoint[0]] 
                if dist > max_dist:
                    max_dist = dist
            if max_dist < min_dist:
                min_dist = max_dist
                candidate_point = datapoint
    return candidate_point























