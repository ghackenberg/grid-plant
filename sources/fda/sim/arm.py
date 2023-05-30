import salabim as sim

from ..model import *
from .machine import *
from .armrobot import *
from .chart import *

class SimArm(sim.Component):
    def __init__(self, corridor: Corridor, machines: list[Machine], name: str, env: sim.Environment, store_in: sim.Store, store_out_1: sim.Store, store_out_2: sim.Store, dx: float, y: float):
        super().__init__(name)

        self.corridor = corridor
        self.machines = machines

        self.env = env

        self.store_in = store_in
        self.store_out_1 = store_out_1
        self.store_out_2 = store_out_2

        # Machines
        self.sim_machines: list[SimMachine] = []
        machine_num = 0
        for machine in machines:
            machine_x = (3 + machine_num * 2) * dx
            sim_machine = SimMachine(machine, env, machine_x, y)
            self.sim_machines.append(sim_machine)
            machine_num = machine_num + 1

        # Transversal robot
        self.sim_arm_robot: list[SimArmRobot] = []
        if len(machines) != 0:
            sim_arm_robot = SimArmRobot(corridor, machines, env, store_in, store_out_1, store_out_2, self.sim_machines, dx, y)
            self.sim_arm_robot.append(sim_arm_robot)

        # Arm horizontal box
        if len(machines) != 0:
            x_len = len(machines) * 2 + 0.26
            x = (0.86 + x_len / 2) * dx
            sim.Animate3dBox(x_len=x_len, y_len=0.25, z_len=0.25, color="green", x=x, y=y, z=2.5)

        # Corridor storage arm vertical box
        if len(machines) != 0:
            sim.Animate3dBox(x_len=0.25, y_len=0.25, z_len=1.5, color="green", x=dx, y=y, z=1.625)
    
    def printStatistics(self):
        print(f"    - Arm {self.name()}:")
        if len(self.machines) != 0:
            for sim_arm_robot in self.sim_arm_robot:
                sim_arm_robot.printStatistics()
        for sim_machine in self.sim_machines:
            sim_machine.printStatistics()
        machineBarChart(self.sim_machines)
        armRobotBarChart(self.sim_arm_robot)


