import salabim as sim
import matplotlib.pyplot as plt

from ..model import Layout, Scenario, Order

from .job import SimJob


class SimOrder(sim.Component):
    def __init__(self, layout: Layout, scenario: Scenario, order: Order, env: sim.Environment, store_start: sim.Store):
        super().__init__()

        self.order = order
        
        self.sim_jobs: list[SimJob] = []
        for i in range(order.quantity):
            sim_job = SimJob(layout, scenario, order, i, env, store_start)
            self.sim_jobs.append(sim_job)

    def printStatistics(self):
        print(f" - {self.order.name}:")
        for sim_job in self.sim_jobs:
            sim_job.printStatistics()
        orderBarChart(self.order, self.sim_jobs)


def orderBarChart(order: Order, jobs: list[SimJob]):
    # Collect categories
    categories = []
    for job in jobs:
        for value in job.state.value.values():
            if value not in categories:
                categories.append(value)
    
    # Compute values
    values = [0 for c in categories]
    for job in jobs:
        for value in job.state.value.values():
            duration = job.state.value.value_duration(value)
            index = categories.index(value)
            values[index] = values[index] + duration

    # Draw chart
    bar_width = 0.15

    # Graph
    for i in range(len(categories)):
        plt.bar(i * bar_width, values[i], width=bar_width, label=categories[i])

    # x Axis
    plt.xticks([])

    # Labels
    plt.xlabel('Order State')
    plt.ylabel('State Duration')
    plt.title(f'{order.name}')

    # Legend
    plt.legend()

    # Print Graph
    plt.show()
