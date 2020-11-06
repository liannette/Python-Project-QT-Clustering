  #!/usr/bin/env python3


###############################################
# 22110 Python and Unix for Bioinformaticians #
#             Project 9: Functions            #
#                                             #
############################################### 



import sys, math


# Get file name and maximum diameter
if len(sys.argv) == 1:
    filename = input("Enter filename: ")
    max_diameter = input("Enter maximum cluster diameter: ")
elif len(sys.argv) == 2: 
    filename = sys.argv[1]
    max_diameter = input("Enter maximum cluster diameter: ")
elif len(sys.argv) == 3: 
    filename = sys.argv[1]
    max_diameter = sys.argv[2]		# ERROR possible
else:
    sys.stderr.write("Usage: QT-clustering.py <filename> <maximum cluster diameter>\n")
    sys.exit(1)



datapoints = []

try:
    infile = open(filename, 'r')
    for line in infile:
        datapoints.append(line.split())
    infile.close()
    
    # Creating a dictionary of all distances 
    distances = dict()
    for point1 in datapoints:
        distances[point1[0]] = dict()
        for point2 in datapoints:
            sum_of_squares = 0
            for dimension in range(len(point1))[1:]: 
                sum_of_squares += (float(point1[dimension]) - float(point2[dimension]))**2
            distances[point1[0]][point2[0]] = sum_of_squares



except IOError as error:
    sys.stderr.write("File I/O error, reason: " + str(error) + "\n")
    sys.exit(1)

   
        


























