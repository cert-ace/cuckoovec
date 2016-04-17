"""
Linear Algebra Utility functions defined for sparse vectors
represented as dictionaries.
"""

import copy
import math

"""
Dot product 
"""
def dict_dot(v1, v2):
    if len(v1) > len(v2):
        tmp = v1; v1 = v2; v2 = tmp

    out = 0.0
    for (k,v) in v1.items():
        out += v * v2.get(k, 0.0)
        
    return out

"""
Performs the operation: v_dst += v_inc * scale
"""
def dict_add_scale(v_dst, v_inc, scale):
    for (k,v) in v_inc.items():
        x = v_dst.get(k, 0.0)
        v_dst[k] = x + scale * v

"""
L2 Norm
"""        
def dict_norm(v):
    return math.sqrt(sum(x*x for x in v.values()))

"""
Performs the operation: v *= scale
"""
def dict_scale(v, scale):
    return {k:val*scale for k,val in v.items()}

"""
Computes component-wise variance of a list of dictionary vectors
"""
def var_dict(X, centered = True):
    mean_x = {}
    mean_x2 = {}
    n = len(X);

    for x in X:
        x2 = {k:v*v for (k,v) in x.items()}
        dict_add_scale(mean_x2, x2, 1.0 / n)

        if centered:
            dict_add_scale(mean_x, x, 1.0 / n)
        
    if centered:
        mean_x_2 = {k:v*v for (k,v) in mean_x.items()}
        dict_add_scale(mean_x2, mean_x_2, -1.0)
        
    return mean_x2

"""
Power iteration on A = YX^TXY^T - U diag(S) U^T
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

def shrink(x, l1_lambda):    
    y = abs(x) - l1_lambda
    if y <= 0.0: return 0.0
    s = 1 if x >= 0.0 else -1
    return s * y

def sparse_power_iteration_4(Y, X, U, S, l1_lambda, iterations, v0):
    vx = copy.deepcopy(v0)
    mu = 1    
    dict_scale(vx, 1.0/dict_norm(vx))
    vy = copy.deepcopy(vx)
    last_obj = -float('inf')

    for i in range(iterations+1):
        # Compute vy := (A * vx) / ||A * vx|| 
        vy1 = {}
        for (x,y) in zip(X,Y):            
            dict_add_scale(vy1, x, dict_dot(vx,y))
                
        vy2 = {}
        for (x,y) in zip(X,Y):
            dict_add_scale(vy2, y, dict_dot(vy1,x))        
        
        for (u,s) in zip(U,S):
            suv = s * dict_dot(u,vx)
            print(suv) 
            dict_add_scale(vy2, u, -suv)        

        mu = dict_norm(vy2)
            
        obj = dict_dot(vy, vy2) - l1_lambda * sum(abs(v) for v in vx.values())
        print('obj={0}'.format(obj))        
        if i > 1 and obj-last_obj < 1e-3 * abs(last_obj):            
            break

        last_obj = obj        
            
        vy2 = dict_scale(vy2, 1.0/mu)
        vy = vy2

        print('mu={0}'.format(mu))
        
        if i < iterations:
            # Compute vx = normalize(shrink(vy' * A))
            vx1 = {}
            for (x,y) in zip(X,Y):            
                dict_add_scale(vx1, x, dict_dot(vy,y))
            
            vx2 = {}
            for (x,y) in zip(X,Y):
                dict_add_scale(vx2, y, dict_dot(vx1,x))        
            
            for (u,s) in zip(U,S):
                suv = s * dict_dot(u,vy)
                dict_add_scale(vx2, u, -suv)        

            print('l0 norm before shrinkage: {0}'.format(len(vx2)))
            vx2 = {k:shrink(v, l1_lambda) for (k,v) in vx2.items()}
            nnz = sum(1 for v in vx2.values() if abs(v) > 0.0)
            print('l0 norm after shrinkage: {0}'.format(nnz))            
                
            vx2 = dict_scale(vx2, 1.0/dict_norm(vx2))
            vx = vx2

    return mu,vx


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
    

    
