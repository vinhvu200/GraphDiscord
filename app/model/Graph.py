import pygal
from app.model import GraphLine
from app.model import GraphPercent


class Graph:
    """
    - This class MUST have self.type, self.timedelta, and self.channel defined in order to generate graphs.
    - The GraphLine objects that are passed in MUST have their coordinates generated
    - Day Graph : message_count vs Time (hours)
    - Week Graph : message_count vs Time (days)
    - Day Percentage Graph : Pie chart of percentages of people's message_count
    - NOTE: Remember that in order to get title for GraphLine object, the object must call generate_coordinates
    """

    # This is to adjust the time to start on a Monday
    # This is used in following methods: __generate_daily_graph_lines(), __generate_weekly_graph_lines()
    days = {'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6}

    def __init__(self, type, channel, timedelta):
        """
        MUST HAVE THESE INITIATED IN ORDER TO WORK
        :param type: 'day' or 'week'
        :param channel: 'general' or 'skype'
        :param timedelta: takes in an integer. 0 indicates current day/week, 1 indicates yesterday/last week,
                            2 indicates two days/weeks ago... etc
        """
        self.type = type
        self.channel = channel
        self.graph_lines = []
        self.rendered_graph = None
        self.timedelta = timedelta

    def __generate_daily_graph(self):
        """
        - This function utilizes the pygal library in order to generate the day graph and render it
        - Day graph : message_count vs time (hour)
        - self.rendered_graph should be okay to use after calling this
        :return: Nothing
        """

        # Initiates the library to use a basic Line Graph
        line_chart = pygal.Line()

        # Format appropriate start and end time to add to the title of the graph
        start_time = ''
        end_time = ''
        if len(self.graph_lines) != 0:
            start_time = '{}/{}/{}'.format(self.graph_lines[0].real_start.month,
                                           self.graph_lines[0].real_start.day,
                                           self.graph_lines[0].real_start.year)
            end_time = '{}/{}/{}'.format(self.graph_lines[len(self.graph_lines)-1].real_end.month,
                                         self.graph_lines[len(self.graph_lines)-1].real_end.day,
                                         self.graph_lines[len(self.graph_lines)-1].real_end.year)

        # Titles the Graph/Chart
        line_chart.title = 'Channel: #{}\nDate: {} -- {}\nMessage Count vs Time (hours)'.format(self.channel,
                                                                                                start_time,
                                                                                                end_time)

        # Names the x_label for each hour in day
        line_chart.x_labels = map(str, range(0, 24))

        # Takes each graph_line in self.graph_lines and add it to the pygal chart
        for graph_line in self.graph_lines:
            line_chart.add(graph_line.title, graph_line.coordinates)

        # Render the graph to be used
        self.rendered_graph = line_chart.render_data_uri()

    def __generate_daily_graph_lines(self):
        """
        - This function generates all the GraphLine objects and stores it into our self.graph_lines variable
        - self.graph_lines will be okay to use after this
        - NOTE: GraphLine.timedelta is for each individual line (example: Monday <- Tuesday <- Wednesday)
                Graph.timedelta is for the whole graph which contains lines ranging from Monday -> Sunday
                so it will give previous Monday -> Sunday
        :return: Nothing
        """

        # Important: This is used to determine the the current day in order to know
        # how to adjust it back to Monday
        graph_line = GraphLine.GraphLine(self.type, self.channel, 0)
        graph_line.generate_coordinates()

        # The start_timedelta will be used to start the graph_line on Monday
        start_timedelta = self.days[graph_line.title]

        # end_timedelta will be used to end graph_line on Sunday
        end_timedelta = 0

        # Adjusted the start/end with initial timedelta
        temp_timedelta = self.timedelta
        while temp_timedelta > 0:
            end_timedelta = start_timedelta + 1
            start_timedelta = start_timedelta + 7
            temp_timedelta -= 1

        # Get all the GraphLine objects between the start/end timedelta, generate
        # the coordinates and stores it into self.graph_lines
        while start_timedelta >= end_timedelta:
            # Create GraphLine object and generate points
            graph_line = GraphLine.GraphLine(self.type, self.channel, start_timedelta)
            graph_line.generate_coordinates()

            # Append to title to let user know it is current day
            if start_timedelta == 0:
                graph_line.title += '(Today)'

            # add into self.graph_lines and decrement start_timedelta
            self.graph_lines.append(graph_line)
            start_timedelta -= 1

    def __generate_weekly_percent_graph(self):

        # Create the graph_percent class and generate the appropriate coordinates
        graph_percent = GraphPercent.GraphPercent(self.type.split('_')[0], self.channel, self.timedelta)
        graph_percent.generate_coordinates()

        # Initiates the library to use a basic Pie Graph
        pie_chart = pygal.Pie()

        # Format appropriate start and end time to add to the title of the graph
        start_time = '{}/{}/{}'.format(graph_percent.real_start.month,
                                           graph_percent.real_start.day,
                                           graph_percent.real_start.year)
        end_time = '{}/{}/{}'.format(graph_percent.real_end.month,
                                     graph_percent.real_end.day,
                                     graph_percent.real_end.year)

        # Titles the Graph/Chart
        pie_chart.title = 'Channel: #{}\nDate: {} - {}\nWeekly User Percentage Activity'.format(self.channel,
                                                                                              start_time,
                                                                                              end_time)

        # Add each name and respective percentage into the pie_chart
        for name, percent in graph_percent.coordinates:
            pie_chart.add(name, round(percent, 2))

        # Set self.rendered_graph
        self.rendered_graph = pie_chart.render_data_uri()

    def __generate_weekly_graph(self):
        """
        - This function utilizes the pygal library in order to generate the week graph and render it
        - Week graph : message_count vs time (day)
        - self.rendered_graph should be okay to use after calling this
        :return:
        """

        # Initiates the library to use a basic Line Graph
        line_chart = pygal.Line()

        # Format appropriate start and end time to add to the title of the graph
        start_time = ''
        end_time = ''
        if len(self.graph_lines) != 0:
            start_time = '{}/{}/{}'.format(self.graph_lines[0].real_start.month,
                                           self.graph_lines[0].real_start.day,
                                           self.graph_lines[0].real_start.year)
            end_time = '{}/{}/{}'.format(self.graph_lines[len(self.graph_lines) - 1].real_end.month,
                                         self.graph_lines[len(self.graph_lines) - 1].real_end.day,
                                         self.graph_lines[len(self.graph_lines) - 1].real_end.year)

        # Titles the Graph/Chart
        line_chart.title = 'Channel: #{}\nDate: {} -- {}\nMessage Count vs Time (days)'.format(self.channel,
                                                                                               start_time,
                                                                                               end_time)

        # All the names for the x_axis
        string_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Names the x_label for each day in weeks
        line_chart.x_labels = map(str, string_day)

        # Takes each graph_line in self.graph_lines and add it to the pygal chart
        for graph_line in self.graph_lines:
            line_chart.add(graph_line.title, graph_line.coordinates)

        # Render the graph to be used
        self.rendered_graph = line_chart.render_data_uri()

    def __generate_weekly_graph_lines(self):
        """
        - This function creates GraphLine objects, generates all its coordinates, and append it
        to self.graph_lines
        - self.graph_lines should be okay to be used after this
        - Generates the lines for the last 4 weeks
        :return:
        """

        # Generates the graph_line object for the last 4 weeks and append them to graph_line
        for timedelta in range(0, 4):
            graph_line = GraphLine.GraphLine(self.type, self.channel, timedelta)
            graph_line.generate_coordinates()
            self.graph_lines.append(graph_line)

    def generate_graph(self):
        """
        - This function checks what self.type of graph the user is trying to generate and
        then redirects to the appropriate private functions
        - It makes sure to clear everything in self.graph_lines first otherwise it will
        just append more stuff the list which makes the new data obsolete
        - The percentage graphs are significantly easier to make because all of its
        percentages have to be computed at once unlike the individual lines for line_charts
        :return: Nothing
        """

        # Clear everything in self.graph_lines
        del self.graph_lines[:]

        # Redirect to appropriate functions
        # Case for day
        if self.type == 'day':
            # Generate all the appropriate line for graph
            self.__generate_daily_graph_lines()
            # Generate the graph with all the lines
            self.__generate_daily_graph()

        # Case for week
        elif self.type == 'week':
            # Generate all the appropriate line for graph
            self.__generate_weekly_graph_lines()
            # Generate the graph with all the lines
            self.__generate_weekly_graph()

        # Case for day_percent
        elif self.type == 'week_percent':
            # Generate percentage graph for the week
            self.__generate_weekly_percent_graph()
