import math
import random
import salabim as sim

class Product(sim.Component):
    def process(self):
        pass

class AbstractRobot(sim.Component):
    def setup(self, base_position: list[float], base_angle: float):
        # State
        self.state = sim.State("state", value = "idle")

        # Frame
        self.base_position = base_position
        self.base_angle = base_angle

        # Joints
        self.joint_angle_ranges = [[0, 0], [-90, 90], [-90, 90]]

        self.source_joint_angles = [0, 0, 0]
        self.target_joint_angles = [0, 0, 0]

        self.source_joint_angles_time = self.env.now()
        self.target_joint_angles_time = self.env.now()

        # Bodies
        self.body_lengths = [50, 50, 50]

        # State label
        self.state_label = sim.AnimateText(
            text = lambda t: self.state.get(),
            x = base_position[0],
            y = lambda t: base_position[1] - 10 if base_angle == 0 else base_position[1] + 10,
            text_anchor = lambda t: "n" if base_angle == 0 else "s"
        )

        # Body lines
        self.body_lines = list(
            map(
                lambda i: sim.AnimateLine(
                    spec = lambda t: self.calculate_body_line_spec(i, t),
                    linecolor = "black",
                    linewidth = 2
                ),
                range(3)
            )
        )

        # Joint circles
        self.joint_circles = list(
            map(
                lambda i: sim.AnimateCircle(
                    x = lambda t: self.calculate_joint_circle_x(i, t),
                    y = lambda t: self.calculate_joint_circle_y(i, t),
                    radius = 5,
                    fillcolor = lambda t: "black" if i < 3 else "blue"
                ),
                range(4)
            )
        )

        # Joint labels
        self.joint_labels = list(
            map(
                lambda i:  sim.AnimateText(
                    text = lambda t: self.calculate_joint_label_text(i, t),
                    x = lambda t: self.calculate_joint_label_x(i, t),
                    y = lambda t: self.calculate_joint_label_y(i, t),
                    text_anchor = "w",
                    textcolor = lambda t: "black" if i < 3 else "blue"
                ),
                range(4)
            )
        )
    
    def calculate_joint_angle_local(self, index: int, time: float):
        # Read source and target angles
        source_joint_angle = self.source_joint_angles[index]
        target_joint_angle = self.target_joint_angles[index]

        # Read source and target angle times
        source_joint_angle_time = self.source_joint_angles_time
        target_joint_angle_time = self.target_joint_angles_time

        # Calculate current angle
        if source_joint_angle_time == target_joint_angle_time:
            # Return constant angle
            return source_joint_angle / 180 * math.pi
        else:
            # Calculate delta between target and source angle
            delta_joint_angle = target_joint_angle - source_joint_angle
            # Calculate delta between target and source angle time
            delta_joint_angle_time = target_joint_angle_time - source_joint_angle_time
            # Calculate animation progrss
            progress = (time - source_joint_angle_time) / delta_joint_angle_time
            # Calculate animation angle
            return (source_joint_angle + delta_joint_angle * progress) / 180 * math.pi
    
    def calculate_joint_angle_world(self, index: int, time: float):
        iter_angle_world = self.base_angle / 180 * math.pi

        # Update angle iteratively
        for i in range(0, index + 1):
            # Update angle
            iter_angle_world = iter_angle_world + self.calculate_joint_angle_local(i, time)

        return iter_angle_world

    def calculate_joint_position_world(self, index: int, time: float):
        iter_position_world = self.base_position.copy()
        iter_angle_world = self.base_angle / 180 * math.pi

        # Update position and angle iteratively
        for i in range(0, index):
            # Read length
            body_length = self.body_lengths[i]

            # Update angle
            iter_angle_world = iter_angle_world + self.calculate_joint_angle_local(i, time)

            # Update position
            iter_position_world[0] = iter_position_world[0] + math.sin(iter_angle_world) * body_length
            iter_position_world[1] = iter_position_world[1] + math.cos(iter_angle_world) * body_length

        return iter_position_world

    def calculate_joint_circle_x(self, index: int, time: float):
        joint_position_world = self.calculate_joint_position_world(index, time)

        return joint_position_world[0]
    
    def calculate_joint_circle_y(self, index: int, time: float):
        joint_position_world = self.calculate_joint_position_world(index, time)

        return joint_position_world[1]

    def calculate_joint_label_x(self, index: int, time: float):
        joint_position_world = self.calculate_joint_position_world(index, time)

        return joint_position_world[0] + 10
    
    def calculate_joint_label_y(self, index: int, time: float):
        joint_position_world = self.calculate_joint_position_world(index, time)

        return joint_position_world[1]
    
    def calculate_joint_label_text(self, index: int, time: float):
        if (index < 3):
            joint_angle_local = self.calculate_joint_angle_local(index, time)

            return f"{round(joint_angle_local / math.pi * 180)}°"
        else:
            joint_position_world = self.calculate_joint_position_world(index, time)

            x = joint_position_world[0]
            y = joint_position_world[1]

            return f"({round(x)} / {round(y)})"

    def calculate_body_line_spec(self, index: int, time: float):
        joint_position_world = self.calculate_joint_position_world(index, time)
        joint_angle_world = self.calculate_joint_angle_world(index, time)

        body_length = self.body_lengths[index]

        x0 = joint_position_world[0]
        y0 = joint_position_world[1]
        x1 = x0 + math.sin(joint_angle_world) * body_length
        y1 = y0 + math.cos(joint_angle_world) * body_length

        return [x0, y0, x1, y1]
    
    def move_to(self, target_joint_angles: list[float], duration: float):
        # Update state
        self.state.set("move")

        # Crop target joint angles
        for i in range(3):
            target_joint_angles[i] = max(target_joint_angles[i], self.joint_angle_ranges[i][0])
            target_joint_angles[i] = min(target_joint_angles[i], self.joint_angle_ranges[i][1])

        # Prepare animation
        self.source_joint_angles_time = self.env.now()

        self.target_joint_angles = target_joint_angles.copy()
        self.target_joint_angles_time = self.env.now() + duration

        # Start process
        self.hold(duration)

        # Finish animation
        self.source_joint_angles = target_joint_angles.copy()
        self.source_joint_angles_time = self.env.now()

        # Update state
        self.state.set("idle")

class ConcreteRobotOne(AbstractRobot):
    def process(self):
        # Define target positions
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
        joint_angles_c = [0, -45, -90]

        # Process loop
        while True:
            # Motion sequence
            self.move_to(joint_angles_b, random.randint(1, 4))
            self.move_to(joint_angles_c, random.randint(1, 8))
            self.move_to(joint_angles_a, random.randint(1, 4))

            print(f"[{self.env.now()}] Roboter holt Produkt")
            self.state.set("pick")
            self.hold(1)
            
            print(f"[{self.env.now()}] Roboter übergibt Produkt an Maschine")
            self.state.set("place")
            self.to_store(robot_to_machine, Product())
            
            print(f"[{self.env.now()}] Roboter wartet auf Produkt von Maschine")
            self.state.set("idle")
            self.from_store(machine_to_robot)
            
            print(f"[{self.env.now()}] Roboter nimmt Produkt von Maschine")
            self.state.set("pick")
            self.hold(1)
            
            print(f"[{self.env.now()}] Roboter gibt Produkt")
            self.state.set("place")
            self.hold(1)

class ConcreteRobotTwo(AbstractRobot):
    def process(self):
        # Define target positions
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Motion sequence
            self.move_to(joint_angles_b, random.randint(1, 4))
            self.move_to(joint_angles_c, random.randint(1, 8))
            self.move_to(joint_angles_a, random.randint(1, 4))

class Machine(sim.Component):
    def setup(self):
        # Define state
        self.state = sim.State("state", "idle")

    def process(self):
        while True:
            print(f"[{self.env.now()}] Maschine wartet auf Produkt von Roboter")
            self.state.set("idle")
            product = self.from_store(robot_to_machine)

            print(f"[{self.env.now()}] Maschine bearbeitet Produkt")
            self.state.set("work")
            self.hold(2)

            print(f"[{self.env.now()}] Maschine übergibt Produkt an Roboter")
            self.to_store(machine_to_robot, product)

# Create simulation environment
env = sim.Environment()
env.modelname("Robotereinsatzplanung")

# Setup 2D or 3D animation
if True:
    # Animation (2D)
    env.animate(True)
    # Window
    env.width(800)
    env.height(600)
    env.position((100, 100))
    # Objects
    sim.AnimateRectangle(
        spec = (0, 0, 800, 100),
        text = "Floor",
        fillcolor = "lightgray",
        textcolor = "black",
        fontsize = 20
    )
    sim.AnimateRectangle(
        spec = (0, 500, 800, 600),
        text = "Ceiling",
        fillcolor = "lightgray",
        textcolor = "black",
        fontsize = 20
    )
else:
    # Animation (3D)
    env.animate3d(True)
    # Window
    env.width3d(800)
    nv.height3d(600)
    env.position3d((100, 100))
    # Objects
    sim.Animate3dGrid(x_range=range(-2, 2, 1), y_range=range(-2, 2, 1))

# Define robots
ConcreteRobotOne(base_position = [200, 100], base_angle = 0)
ConcreteRobotTwo(base_position = [400, 100], base_angle = 0)
ConcreteRobotTwo(base_position = [600, 100], base_angle = 0)
ConcreteRobotTwo(base_position = [200, 500], base_angle = 180)
ConcreteRobotTwo(base_position = [400, 500], base_angle = 180)
ConcreteRobotTwo(base_position = [600, 500], base_angle = 180)
# Define machines
Machine()
# Define stores
robot_to_machine = sim.Store()
machine_to_robot = sim.Store()

# Start simulation with/without video production
if True:
    # Video production disabled
    env.run(sim.inf)
else:
    # Video production enabled
    env.video("test.mp4")
    env.run(till = 30)
    env.video_close()