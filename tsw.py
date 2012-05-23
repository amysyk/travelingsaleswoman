#Explicit importing makes it more clear what a user needs to define
#versus what is included within the pyomo library
from coopr.pyomo import (ConcreteModel, Objective, Var, NonNegativeIntegers,
                              minimize, Constraint)

#Set nodes
Locations = ['Apple', 'Cisco', 'CVS', 'Ebay']

#Set arc lengths

'''Distances = {('Apple','Apple'):0,
('Apple','Cisco'):0.138202084184728,
('Apple','CVS'):0.443699720914948,
('Apple','Ebay'):0.138202084184728,
('Cisco','Apple'):0.138202084184728,
('Cisco','Cisco'):0,
('Cisco','CVS'):0.426320750769892,
('Cisco','Ebay'):0,
('CVS','Apple'):0.443699720914948,
('CVS','Cisco'):0.426320750769892,
('CVS','CVS'):0,
('CVS','Ebay'):0.426320750769892,
('Ebay','Apple'):0.138202084184728,
('Ebay','Cisco'):0,
('Ebay','CVS'):0.426320750769892,
('Ebay','Ebay'):0}'''

#Set OnRoute Matrix

OnRoute = [0,0,0,0,
           0,0,0,0,
           0,0,0,0,
           0,0,0,0]

#Set Distance Matrix
Distances = [0.00,0.14,0.44,0.14,
             0.14,0.00,0.43,0.00,
             0.44,0.43,0.00,0.43,
             0.14,0.00,0.43,0.00]

#Concrete Model
model = ConcreteModel()

#Decision Variables
model.OnRoute = Var(OnRoute, within=NonNegativeIntegers)

#Objective
model.obj = Objective(expr=
            sum(Distances[i] * model.OnRoute[i] for i in range(len(Distances))),
            sense = minimize)


#test

print model.OnRoute
