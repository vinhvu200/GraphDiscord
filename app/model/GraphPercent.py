from app.model import GraphLine
from database import get_db


class GraphPercent(GraphLine.GraphLine):
    """
    - This class inherits from GraphLine to use the get_time_range() function and reuse all variables
    - The only difference in this is that the coordinates are stored in a dictionary. The reason for
        this is comes down to how percentages are calculated (Name : Percentage) instead of having
        a list of coordinates
    """

    def __init__(self, interval, channel, timedelta):
        super().__init__(interval, channel, timedelta)
        self.coordinates = dict()

    def __generate_title_week(self):
        """
        - This function generates the title for the Graph
        - This is to follow the naming conventions used in the GraphLine class.
            GraphLine class requires more work to generate its title
        :return: None
        """
        self.title = 'Channel:#{}\nWeekly Percentage'.format(self.channel)

    def __generate_coordinates_week(self):
        self.__query_results()
        self.__calculate_weekly_activities_percentage()

    def __query_results(self):
        """
        - This function gets the appropriate time range and attempts to query the data
        - The results will be stored in self.query_results
        :return: None
        """

        # Get appropriate time range
        utc_start, utc_end, real_start, real_end = self.get_time_range()

        # Open client to access database
        client, db, collection = get_db()

        # Attempt to query by dates
        try:
            self.query_results = collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': self.channel})
        except Exception as e:
            print(e)

        self.__calculate_weekly_activities_percentage()

    def __calculate_weekly_activities_percentage(self):

        message_count = 0
        for query in self.query_results:
            message_count += 1
            name = query['author'].split('#')[0]
            if name in self.coordinates:
                self.coordinates[name] += 1
            else:
                self.coordinates[name] = 1

        for activity in self.coordinates:
            self.coordinates[activity] = self.coordinates[activity] / message_count * 100

    def generate_coordinates(self):

        self.coordinates.clear()

        if self.interval == 'week':
            self.__generate_title_week()
            self.__generate_coordinates_week()