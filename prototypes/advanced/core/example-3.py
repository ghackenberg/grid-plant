from fda import *


# Create machine types
machineType1 = MachineType('Machine type 1', 1)
machineType2 = MachineType('Machine type 2', 2)
machineType3 = MachineType('Machine type 3', 3)
machineType4 = MachineType('Machine type 4', 4)


# Create tool types
toolType1 = ToolType('Tool type 1', 1, 2, 3, 10)
toolType2 = ToolType('Tool type 2', 2, 1, 2, 9)
toolType3 = ToolType('Tool type 3', 3, 3, 4, 12)


# Create Product Type
productType1 = ProductType('Product Type 1', 12, 12, 12, 5)
productType2 = ProductType('Product Type 2', 12, 24, 11, 10)
productType3 = ProductType('Product Type 3', 14, 15, 15, 6)
productType4 = ProductType('Product Type 4', 22, 23, 12, 7)
productType5 = ProductType('Product Type 5', 22, 23, 12, 7)
productType6 = ProductType('Product Type 6', 12, 24, 11, 10)

# Create Process Steps
processSteps1 = ProcessStep('Process 1', 20, 20, 0.15, machineType1, toolType1, productType1, productType2)
processSteps1_2 = ProcessStep('Process 1.2', 15, 24, 0.20, machineType1, toolType2, productType3, productType2)
processSteps2 = ProcessStep('Process 2', 10, 24, 0.11, machineType2, toolType3, productType2, productType4)
processSteps3 = ProcessStep('Process 3', 10, 24, 0.11, machineType3, toolType2, productType2, productType5)
processSteps4 = ProcessStep('Process 4', 10, 24, 0.11, machineType4, toolType1, productType2, productType6)


#Create Scenario
scenario1 = Scenario('Scenario 1') #Best Case
scenario2 = Scenario('Scenario 2') #Middle Case
scenario3 = Scenario('Scenario 3') #Worst Case



# Create CustomerOrder
order1 = Order(1, 30, 11, 20, productType6, scenario1)
order1_2 = Order(1, 40, 15, 30, productType2,  scenario1)
order2 = Order(2, 400, 25, 30, productType2,  scenario2)
order3 = Order(3, 500, 15, 20, productType4,  scenario3)
order4 = Order(4, 300, 25, 30, productType5,  scenario3)


#Create Layout
layout1 = Layout('Layout 1',  10, 5) #Best Case
layout2 = Layout('Layout 2',  11, 3) #Middle Case
layout3 = Layout('Layout 3',  11, 3) #Worst Case

#Create T_Corridor
corridor1 = Corridor(1, 500,  layout1)
corridor2 = Corridor(2, 350,  layout1)
corridor3 = Corridor(3, 200,  layout1)
corridor4 = Corridor(4, 150,  layout2)
corridor5 = Corridor(5, 150,  layout2)
corridor6 = Corridor(6, 350,  layout3)
corridor7 = Corridor(7, 120, layout3)
corridor8 = Corridor(8, 150, layout3)
corridor9 = Corridor(9, 300, layout3)


# Create machines
machine1_1 = Machine('Machine 1.1', machineType1, corridor1)
machine1_2 = Machine('Machine 1.2', machineType1, corridor1)
machine1_3 = Machine('Machine 1.3', machineType1, corridor3)
machine1_4 = Machine('Machine 1.4', machineType1, corridor3)
machine1_5 = Machine('Machine 1.5', machineType1, corridor4)
machine1_6 = Machine('Machine 1.6', machineType1, corridor4)
machine1_7 = Machine('Machine 1.7', machineType1, corridor5)
machine1_8 = Machine('Machine 1.8', machineType1, corridor5)
machine1_9 = Machine('Machine 1.9', machineType1, corridor6)
machine1_10 = Machine('Machine 1.10', machineType1, corridor6)

machine2_1 = Machine('Machine 2.1', machineType2, corridor2)
machine2_2 = Machine('Machine 2.2', machineType2, corridor4)
machine2_3 = Machine('Machine 2.3', machineType2, corridor5)
machine2_4 = Machine('Machine 2.4', machineType2, corridor7)

machine3_1 = Machine('Machine 3.1', machineType3, corridor2)
machine3_2 = Machine('Machine 3.2', machineType3, corridor4)
machine3_3 = Machine('Machine 3.3', machineType3, corridor5)
machine3_4 = Machine('Machine 3.4', machineType3, corridor8)

machine4_1 = Machine('Machine 4.1', machineType4, corridor2)
machine4_2 = Machine('Machine 4.2', machineType4, corridor4)
machine4_3 = Machine('Machine 4.3', machineType4, corridor5)
machine4_4 = Machine('Machine 4.4', machineType4, corridor9)

#Create Simulation
simulation1 = Simulation(1, layout1, scenario1)
simulation2 = Simulation(2, layout2, scenario2)
simulation3 = Simulation(3, layout3, scenario3)



toNetworkXMinimal()


#for ProcessSteps in ProductType2.producingProcessSteps:
   # print(ProcessSteps.name + " can produce " + ProductType2.name)






