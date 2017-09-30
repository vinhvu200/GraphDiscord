import pygal


class Graph:
    """
    - This class MUST have self.type and self.channel defined in order to generate graphs.
    - The self.graph_lines variable MUST contain objects for GraphLine class
    """
    def __init__(self, type, channel):
        self.type = type
        self.channel = channel
        self.graph_lines = []
        self.rendered_graph = None

    def add_graph_line(self, graph_line):
        self.graph_lines.append(graph_line)

    def clear_graph_lines(self):
        del self.graph_lines[:]

    def generate_graph(self):

        if self.type == 'daily':
            self.__generate_daily_graph()
        elif self.type == 'weekly':
            self.__generate_weekly_graph()

    def __generate_daily_graph(self):
        line_chart = pygal.Line()
        line_chart.title = 'Channel: #{}\nMessage Count vs Time (hours)'.format(self.channel)
        line_chart.x_labels = map(str, range(0, 24))

        for graph_line in self.graph_lines:
            line_chart.add(graph_line.title, graph_line.coordinates)

        self.rendered_graph = line_chart.render_data_uri()

    def __generate_weekly_graph(self):
        pass