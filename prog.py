from mpi4py import MPI
import numpy as np
import glob
import glob


comm = MPI.COMM_WORLD
size = comm.Get_size() # total number of processes
rank = comm.Get_rank()

# 1. list all text files in the directory
rel_filepaths = glob.glob("*.txt")

# 2. (optional) create a function to read the number of rows in a file
def count_rows_one(filepath):
  res = 0
  if len(filepath) == 0:
    res = 0
  else:
    f = open(filepath, 'r')
    res = len(f.readlines())
    f.close()

  return res

def count_rows(filepaths):
  res = 0
  ress = []
  for filepath in filepaths:
    f = open(filepath, 'r')
    res = len(f.readlines())
    ress.append(res)
    f.close()
  
  return ress
M = len(rel_filepaths)
if M > size:
  files_chunks = [ rel_filepaths[int(i*M/size):int((i+1)*M/size )] for i in range(size)]
  if rank == 0:
    s = [max(count_rows(filepath)) for filepath in files_chunks]
  else:
    s = None
elif M == size:
  files_chunks = rel_filepaths
  if rank == 0:
    s = [count_rows_one(filepath) for filepath in files_chunks]
  else:
    s = None
else: 
  emp = ['' for i in range(size - M)]
  files_chunks  = rel_filepaths+emp

  if rank == 0:
    s = [count_rows_one(filepath) for filepath in files_chunks]
  else:
    s = None
# process 1 sends its partial sum to process 0


    
data = comm.scatter(s, root=0)

res = comm.reduce(data, op = MPI.MAX, root = 0)   
if rank == 0:
    result = res 
    print ('Max size:', result)
