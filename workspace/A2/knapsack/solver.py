#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


def knapSack(capacity, wt, val, item_count):
    K = [[0 for x in range(capacity + 1)] for x in range(item_count + 1)]

    # Build table K[][] in bottom up manner
    for i in range(item_count + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    return K[item_count][capacity]


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    wt = []
    val = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
        val.append(int(parts[0]))
        wt.append(int(parts[1]))

    taken = [0] * len(items)
    value = knapSack(capacity, wt, val, item_count)
    print(value)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    # value = 0
    # weight = 0
    # taken = [0] * len(items)
    #
    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys

    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    file_location = 'data/ks_4_0'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
    # else:
    #     print(
    #         'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
