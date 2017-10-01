import pygal
from app.model import GraphLine


class Graph:
    """
    - This class MUST have self.type and self.channel defined in order to generate graphs.
    - The self.graph_lines variable MUST contain objects for GraphLine class
    """
    def __init__(self, type, channel, timedelta):
        self.type = type
        self.channel = channel
        self.graph_lines = []
        self.rendered_graph = None
        self.timedelta = timedelta

    def __add_graph_line(self, graph_line):
        self.graph_lines.append(graph_line)

    def clear_graph_lines(self):
        del self.graph_lines[:]

    def __generate_daily_graph(self):
        line_chart = pygal.Line()
        line_chart.title = 'Channel: #{}\nMessage Count vs Time (hours)'.format(self.channel)
        line_chart.x_labels = map(str, range(0, 24))

        for graph_line in self.graph_lines:
            line_chart.add(graph_line.title, graph_line.coordinates)

        self.rendered_graph = line_chart.render_data_uri()

    def __generate_daily_graph_lines(self):

        days = {'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5,
                'Sunday': 6}

        graph_line = GraphLine.GraphLine('day', 'skype', 0)
        graph_line.generate_coordinates()

        start_index = days[graph_line.title]

        while start_index >= 0:
            graph_line = GraphLine.GraphLine('day', 'skype', start_index)
            graph_line.generate_coordinates()

            self.__add_graph_line(graph_line)
            start_index -= 1

    def generate_graph(self):

        if self.type == 'day':
            self.__generate_daily_graph_lines()
            self.__generate_daily_graph()
        elif self.type == 'week':
            self.__generate_weekly_graph_lines()
            self.__generate_weekly_graph()

    def __generate_weekly_graph_lines(self):
        pass

    def __generate_weekly_graph(self):
        pass
