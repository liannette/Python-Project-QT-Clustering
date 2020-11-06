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
    max_distance = 0
    distances = dict()
    for point1 in datapoints:
        distances[point1[0]] = dict()
        for point2 in datapoints:
            distance = calculate_distance(point1, point2)
            distances[point1[0]][point2[0]] = distance
            if distance > max_distance:
                max_distance = distance
    
    # Getting maximum diameter
    if '%' in max_diameter:
        max_diameter = float(max_diameter[:-1])/100 * max_distance
    else: 
        max_diameter = float(max_diameter)

except IOError as error:
    sys.stderr.write("File I/O error, reason: " + str(error) + "\n")
    sys.exit(1)
   
 
#print(distances[datapoints[0][0]])



























