#!/usr/bin/env python

'''
Floyd Warshall Parallel Assignment : Find all shortest paths between all points.

@author Briana Cervantes
'''

import argparse
import numpy as np
import matrixUtils as mu
from mpi4py import MPI
from timeit import default_timer as timer


def calculate_path(graph, expected_result):
    '''
    Calculates the shortest path for all points
    '''

    comm       = MPI.COMM_WORLD
    rank       = comm.Get_rank()
    size       = comm.Get_size()
    print("size: ", size)
    print("rank: ", rank)
    rows       = len(graph)
    rows_per_thread = rows / size
    start      = int(rows_per_thread * rank)
    end        = int(rows_per_thread * (rank + 1))
    startTime  = timer()

    for i in range(rows):
        owner = int((size/rows) * i )
        graph[i] = comm.bcast(graph[i], root=owner)

        for k in range(start, end):
            for j in range(rows):
                graph[k][j] = min(graph[k][j], graph[k][i] + graph[i][j])

    # Bring everything together
    if rank is 0:
        for i in range(end, rows):
            owner = int((size/rows) * i)
            graph[i] = comm.recv(source=owner, tag=i)
        endTime = timer()
        mu.writeToFile(graph, "result.txt")
        if (graph == expected_result):
            mu.printSubarray(expected_result)
            print("Success!")
            print("Total Time: ", endTime - startTime)
        else:
            print("Try again!")
    else:
        for i in range(start, end):
            comm.send(graph[i], dest = 0, tag = i)



def main():
    '''
    Used for running as a script
    '''

    parser = argparse.ArgumentParser(description =
        'Generate a graph from a file.')
    parser.add_argument('-f', '--filename', default = 'fwTest.txt',
            help = 'The name of the file to read from')
    parser.add_argument('-r', '--resultfile', default = 'fwTestResult.txt',
            help = 'The name of the file to read the result from')

    args = parser.parse_args()

    if (args.filename is not None):
        graph = mu.readFromFile(args.filename)

        if (args.resultfile is not None):
            expected_result = mu.readFromFile(args.resultfile)
            calculate_path(graph, expected_result)


if __name__ == '__main__':
    main()
