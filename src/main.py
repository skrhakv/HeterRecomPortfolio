#!/usr/bin/python3

import time
import sys
import os

import random
import numpy as np

from execute.executeBatches import executeBatches #function
from execute.generateBatches import generateBatches #function
from execute.generateBehaviour import generateBehaviour #function


def main2():

  start = time.time()


  executeBatches()


  end = time.time()

  print()
  print("Time: " + format(end - start, '.5f') + " s")


if __name__ == "__main__":

  np.random.seed(42)
  random.seed(42)

  if len(sys.argv) == 2 and sys.argv[1] == "-generateBatches":
      generateBatches()

  if len(sys.argv) == 2 and sys.argv[1] == "-generateBehaviours":
      generateBehaviour()

  if len(sys.argv) == 1:
      main2()
