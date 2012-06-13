from coopr.pyomo import *

# create a model root
model = AbstractModel()

# set bounds:
# n - number of nodes
# max_out - number of arcs out of each node
# max_in - number of arcs in each node
# arc_to_self - number of arcs to self allowed
# min_arcs_between_subsets - number of arcs between any subset of nodes
model.n = Param(within=NonNegativeIntegers)
model.max_out = Param(within=NonNegativeIntegers)
model.max_in = Param(within=NonNegativeIntegers)
model.arc_to_self = Param(within=NonNegativeIntegers)

# create index sets:
# i = 1,..., n
# j = 1,..., n
# i,j for each i and j combination
model.I = RangeSet(0, model.n)
model.J = RangeSet(0, model.n)
model.IJ = model.I * model.J

# create distance parameter for each i and j combination
model.d = Param(model.I, model.J)

# declare a variable indexed by the set IJ
model.x = Var(model.IJ, within=Binary)

# declare objective function Dij * Xij
def obj_expression(model):
    return summation(model.d, model.x)

# declare objective variable
model.OBJ = Objective(rule=obj_expression)

# declare constraint: one and only one arc out of each node
def xi_constraint_rule(model, i):
    return sum(model.x[i,j] for j in model.J) >= model.max_out
model.xiConstraint = Constraint(model.I, rule=xi_constraint_rule)


# declare constraint: one and only one arc in each node
def xj_constraint_rule(model, j):
    return sum(model.x[i,j] for i in model.I) >= model.max_in
model.xjConstraint = Constraint(model.J, rule=xj_constraint_rule)


# declare constraint: no arcs to self
def arc_to_self_constraint_rule(model, i):
    return model.x[i,i] == model.arc_to_self
model.arcToSelfConstraint = Constraint(model.I, rule=arc_to_self_constraint_rule)


# declare constraint: no 2-node subtours
def sub2_init(model):
    return ((i,j) for i in model.I for j in model.I if i!=j)
model.sub2 = Set(dimen=2, initialize=sub2_init)

def sub2_rule(model,i,j):
    return model.x[i,j] + model.x[j,i] <= 1
model.sub2contraint = Constraint(model.sub2, rule=sub2_rule)

# declare constraint: no 3-node subtours
def sub3_init(model):
    return ((i,j,k) for i in model.I for j in model.I for k in model.I if (i!=j and i!=k and j!=k))
model.sub3 = Set(dimen=3, initialize=sub3_init)

def sub3_rule(model,i,j,k):
    return model.x[i,j] + model.x[j,i] + model.x[i,k] + model.x[k,i] + model.x[k,j] + model.x[j,k] <= 2
model.sub3constraint = Constraint(model.sub3, rule=sub3_rule)