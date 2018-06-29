import argparse
from threading import Thread,enumerate
import datetime
import sys
sys.path.insert(0, '../')
import k_canalyzing_not_faulty as kc
import pyximport
pyximport.install()
import find_attractors_dfs as fad
import time

#start=time.time()
parser = argparse.ArgumentParser(description='Make a discrete dynamical system at random given the number of variables and canalyzing depth.')
parser.add_argument('num', type= int)
parser.add_argument('cores', type=int)
parser.add_argument('num_vars', type= int)
parser.add_argument('canalyzing_depth', type=int)
args = parser.parse_args()

def threadfunc():
    funcs=[]
    for i in range(args.num_vars):
        funcs.append(kc.random_k_canalyzing(args.num_vars, args.canalyzing_depth).return_truth_table())
    tuples=fad.find_attractors_and_basins(funcs)

    with open("num_vars="+str(args.num_vars)+"_depth="+str(args.canalyzing_depth)+".txt", "a") as file:
        print >>file, str(tuples)

i=0
a=[]
while(i<args.num):
    if(len(enumerate())<args.cores):
        a.append(Thread(None,threadfunc,None))
        a[-1].start()
        i+=1
for j in a:
    j.join()

#end=time.time()
#print(end-start)