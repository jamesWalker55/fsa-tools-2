# graph a
a_formal = "({a, b}, {q0 , q1 , q2 }, {(q0 , a, q0), (q0 , b, q0 ), (q0 , b, q1 ), (q1, a, q2 ), (q1 , b, q2 )}, q0, {q1 , q2 })"

a_informal = """
start 0
end 1 2
0 a 0
0 b 0
0 b 1
1 a 2
1 b 2
"""

# graph b
b_informal = """
start 0
end 0
0 e 1
0 b 2
1 a 0
2 a 1
2 b 1
2 a 2
"""

# graph c
c_informal = """
start q0
end q1 q1
q0 b q1
q1 a q1
q1 b q2
q2 a q2
q2 b q1
q1 a q1
q1 b q2
"""

# graph d
d_formal = "({0, 2, 4}, {q0 , q1 , q2 , q3 },  {(q0 , 0, q1 ), (q0, 0, q2 ), (q0, 4, q3), (q1 , 2, q1), (q1 , 2, q2 ), (q2 , 4, q2 ), (q2 , 2, q3 ), (q3 , 2, q2 )}, q0 , {q2 })"

# graph e
# non-deterministic
e_formal = "({a, b}, {q0 , q1 , q2 }, {(q0 , a, q0), (q0 , b, q0 ), (q0 , b, q1 ), (q1, a, q2 ), (q1 , b, q2 )}, q0, {q1 , q2 })"

# graph f
f_informal = """
start q0
end q3
q0 0 q1
q0 0 q3
q0 1 q3
q1 1 q2
q1 1 q3
q2 0 q3
q3 0 q3
"""

# graph g
g_informal = """
start x
end y z
x a x
x b x
x a y
x a z
y b y
z c z
"""
