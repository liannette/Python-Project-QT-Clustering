# QT clustering
## Description

The program reads a number of data points (multi-dimensional vectors) from a file and partitions those into clusters. Clustering is important in discovering patterns or modes in multi-dimensional data sets. It is also a method of organizing data examples into similar groups (clusters). In this particular case, QT clustering partitions the data set such that each example (data point) is assigned to exactly one cluster. QT clustering is superior to K-means clustering in that the number of clusters is not given beforehand and it yields the same result in repeated runs. It requires more CPU time, though.

QT (Quality Threshold) has its name from the user-determined threshold (distance) of the maximal diameter of the clusters that the method computes.
## Input and output

The input is a tab separated file containing one data point on each line. Each data point is a vector consisting of a number of numbers. The program should handle any given vector size, but the vector size is constant in any data file. Input file example:

    ex01	8.76	3.29	1.05
    ex02	12.3	2.33	3.53
    ex03	-0.54	-3.56	1.45
    .
    .

The output is all data points, partitioned in the clusters they belong to. Output example where each cluster starts with the cluster and is proceeded by the the members of that cluster:

    Cluster-1
    ex10	1.04	2.98	1.34
    ex12	1.23	2.34	1.69
    .
    .
    Cluster-2
    ex04	-0.34	3.51	9.02
    ex07	-8.56	5.12	12.5
    .
    .

## Examples of program execution

    cluster.py vectors.txt 500

The 500 is the maximum diameter for a cluster in the data set. An interesting twist could be to automatically decide the cluster diameter like this: X % of the distance between the two data point furthest away from each other. Called like this

    cluster.py vectors.txt 30%

## Details

The method works for any type of data set where it is possible to calculate a distance between any two points. In this project we are just considering euclidean distances, as they are simple. Pythagoras's theorem.

The algorithm works like this.

  1. For each point in the data set, calculate the candidate cluster with that point as the starting point. With n points in the data set, there are n candidate clusters, obviously.
  2. Choose the candidate cluster that contains most points as the primary cluster and remove those points from the data set. If two or more candidate clusters have equally most points, pick the cluster with the smallest diameter. If they are still equal, pick the first you found.
  3. Repeat step 1 and 2 until there are no points in the data set or a set limit has been reached; like all remaining candidate clusters has less than, say, 10 points and are therefore not true clusters, but noise.
  4. Print the resulting clusters.

A candidate cluster for a point is calculated using "complete linkage" like this:

  1. Consider the starting point as the beginning of the candidate cluster for that point. This is trivially seen as a subset of your data set.
  2. Add one point from your data set at a time in such a way that you extend the candidate cluster diameter the least. Again, if two points would extend the diameter the least, pick the first one you find.
  3. Continue adding points - that is repeat step 2 - to your candidate cluster until the diameter exceeds the Quality Threshold (hence the name QT clustering). The point that makes the diameter exceed the QT is not part of the candidate cluster.

Important definition: The diameter of a data set (or candidate cluster) is the distance of the two points furthest from each other.
Note: All points in the data set can participate in multiple candidate clusters. Any point is not permanently assigned to a candidate cluster, before you actually pick the largest one and remove the "winners" points from the data set.
Note: Building a candidate cluster according to above method is NOT the same method as adding the nearest point to the starting point or any point in the growing candidate cluster (which is wrong).

A fairly large part of this project is optimizing the algorithm just described. This is done by gaining insight in the algorithm - not calculating what does not need to be calculated, not calculating the same thing again and again.

Various data sets: 100 data points, 1000 data points, 4169 data points, 5000 data points, 6000 data points, 10000 data points. 

Checking the correctness of your program.
Result of clustering the small list with QT being 30% of the diameter.
Result of clustering 1000 points with QT being 30% of the diameter.

The algorithm is deterministic - meaning that an implementation will yield the same result on the same data set every time. However, in the description there are two places, where "you pick the first one" you find. This is implementation dependent and therefore two different implementations of QT can give rise to different results. The data sets given here are constructed in such a way, that this will NOT happen for them, i.e. no matter how you implement your method you should get the same result.
## References:
  1. Exploring expression data: identification and analysis of coexpressed genes. LJ Heyer, S Kruglyak, S Yooseph - Genome research, 1999 - genome.cshlp.org
  2. QT clustering in industry - Agilent
