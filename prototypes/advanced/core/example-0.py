from fda import *


# Create machine types
machineType1 = MachineType('Machine type 1', 1)


# Create tool types
toolType1 = ToolType('Tool type 1', 1, 2, 3, 10)
toolType2 = ToolType('Tool type 2', 2, 1, 2, 9)


# Create Product Type
productType1 = ProductType('Product Type 1', 12, 12, 12, 5)
productType2 = ProductType('Product Type 2', 12, 24, 11, 10)
productType3 = ProductType('Product Type 3', 14, 15, 15, 6)


# Create Process Steps
processSteps1 = ProcessStep('Process 1', 20, 20, 0.15, machineType1, toolType1, productType1, productType2)
processSteps2 = ProcessStep('Process 2', 15, 24, 0.20, machineType1, toolType2, productType1, productType3)


#Create Customer
customer1 = Customer('Rossi', 'Roma', 1)


#Create Scenario
scenario1 = Scenario('Scenario 1')


#Create CustomerOrder
order1 = Order(1, 10, 11, 20, productType2, customer1, scenario1)
order2 = Order(2, 10, 11, 20, productType3, customer1, scenario1)


#Create Layout
layout1= Layout('Layout 1', 200, 10, 5, 4)


#Create T_Corridor
corridor1 = Corridor(1, 2, layout1)


# Create machines
machine1_1 = Machine('Machine 1.1', machineType1, corridor1)
machine1_2 = Machine('Machine 1.2', machineType1, corridor1)


#Create Simulation
simulation1 = Simulation(1, layout1, scenario1)


toNetworkX()


#for ProcessSteps in ProductType2.producingProcessSteps:
    #print(ProcessSteps.name + " can produce " + ProductType2.name)