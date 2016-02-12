"""
Linear Algebra Utility functions defined for sparse vectors
represented as dictionaries.
"""

import copy
import math

def dict_dot(v1, v2):
    if len(v1) > len(v2):
        tmp = v1; v1 = v2; v2 = tmp

    out = 0.0
    for (k,v) in v1.items():
        out += v * v2.get(k, 0.0)
        
    return out

def dict_add_scale(v_dst, v_inc, scale):
    for (k,v) in v_inc.items():
        x = v_dst.get(k, 0.0)
        v_dst[k] = x + scale * v

def dict_norm(v):
    return math.sqrt(sum(x*x for x in v.values()))

def dict_scale(v, scale):
    return {k:val*scale for k,val in v.items()}

"""
Power iteration on YX^TXY^T - U diag(S) U^T
where X,Y and U are lists of column vectors and S is a list of scalars 

Additioanl parameters:
 iterations: Number of iterations
 v0: Initial eigen vector

Returns:
 A tuple (top eigen value, top eigen vector) 
"""
def power_iteration_4(Y, X, U, S, iterations, v0):
    v = copy.deepcopy(v0)

    for i in range(iterations):
        v1 = {}
        for (x,y) in zip(X,Y):            
            dict_add_scale(v1, x, dict_dot(v,y))
                
        v2 = {}
        for (x,y) in zip(X,Y):
            dict_add_scale(v2, y, dict_dot(v1,x))        
        
        for (u,s) in zip(U,S):
            print(-s * dict_dot(u,v)) 
            dict_add_scale(v2, u, -s * dict_dot(u,v))        
            
        mu = dict_norm(v2)
        v2 = dict_scale(v2, 1.0/mu)
        v = v2

    return mu,v
    
if __name__ == "__main__":
#if True:
    # dot product
    a = {'a' : 1, 'b' : 2}
    b = {'a' : -1, 'c' : 4}
    assert dict_dot(a,b) == -1

    # add scale
    a = {'a' : 1, 'b' : 2}
    b = {'a' : -1, 'c' : 4}
    dict_add_scale(a,b,2.0)
    assert a['a'] == -1
    assert a['b'] == 2
    assert a['c'] == 8
    assert len(a) == 3
    
    # norm
    a = {'a' : 3, 'b' : 4}
    assert dict_norm(a) == 5

    # scale
    a = {'a' : 1, 'b' : 2}
    b = dict_scale(a, -2)
    assert b['a'] == -2
    assert b['b'] == -4
    assert len(b) == 2

    print("All tests done")
    
