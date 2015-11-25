from cuckoovec import CuckooVector
from cuckoovec import CuckooMatrix

#Computes vv^T
def r1_from_vector(v):
    m = CuckooMatrix()

    lst = [(key,val) for key,val in v.items()]
        
    for key,val in lst:
        for k2,v2 in lst:
            m[key,k2] = val * v2
        
    return m

# m += scale * uv^T
def add_r1_matrix(m, u, v, scale):
    lst = [(key,val) for key,val in v.items()]
    
    for key,val in lst:
        col = m.get_or_insert_col(key)
        col.add_scale(u, val * scale)

# Compute MM^T
def mmt(m):
    m_out = CuckooMatrix()

    for key,col in m.columns():
        add_r1_matrix(m_out, col, col, 1.0)

    return m_out

def sum_columns(m):
    v = CuckooVector({})

    for key,col in m.columns():
        v.add(col)

    return v

def power_iteration(m, iterations, v0):
    v = CuckooVector({})
    v.add(v0)

    for i in range(iterations):
        v = m.mult_vec(v)
        mu = v.norm(2)
        v.scale(1.0/mu)
        
    return mu,v

# Power iteration for mmt where m is a list of column vectors
def power_iteration_mmt(m, iterations, v0):
    v = CuckooVector({})
    v.add(v0)

    for i in range(iterations):
        vp = CuckooVector({})
        for c in m:
            vp.add_scale(c, c.dot(v))

        mu = v.norm(2)        
        vp.scale(1.0/mu)
        v = vp
        
    return mu,v
        
#r1 matrix
c = CuckooVector({})
c['w1'] = 2.0;
c['w2'] = 3.0;
m = CuckooMatrix()
add_r1_matrix(m, c, c, 1.0)

assert m['w1', 'w1'] == 4.0
assert m['w2', 'w1'] == 6.0
assert m['w1', 'w2'] == 6.0
assert m['w2', 'w2'] == 9.0

#get_col
m.clear()
m['w2','w2'] = 5.0
assert m.get_col('w1') is None
assert m.get_col('w2')['w2'] == 5.0

#mmt
m.clear()
m['w1','w1'] = 1.0
m['w2','w1'] = 2.0
m = mmt(m)

assert m['w1', 'w1'] == 1.0
assert m['w2', 'w1'] == 2.0
assert m['w1', 'w2'] == 2.0
assert m['w2', 'w2'] == 4.0


#power iteration
c = CuckooVector({})
c['w1'] = 1.0;
c['w2'] = 1.0;
m = CuckooMatrix()
add_r1_matrix(m, c, c, 1.0)

c['w1'] = 2.0;
c['w2'] = -2.0;
add_r1_matrix(m, c, c, 1.0)

v0 = sum_columns(m)
v0['w2'] = 0.3
mu,u = power_iteration(m, 10, v0)
print(mu)
print(u['w1'])
print(u['w2'])

add_r1_matrix(m, u, u, -mu)
mu,u = power_iteration(m, 10, v0)
print(mu)
print(u['w1'])
print(u['w2'])

