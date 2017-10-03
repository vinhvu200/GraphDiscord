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

    def __calculate_weekly_activities_percentage(self):
        """
        - This function takes all the results in self.query_results, count up the total messages,
            and put each unique name in the dictionary to count their individual message_count
        - Afterward, it divides each unique name's individual message_count by the total and multiplies
            by 100 to get the appropriate percentage
        :return: None
        """
        message_count = 0
        unsorted_coordinates = dict()
        for result in self.query_results:
            message_count += 1
            name = result['author'].split('#')[0]
            if name in unsorted_coordinates:
                unsorted_coordinates[name] += 1
            else:
                unsorted_coordinates[name] = 1

        for name in unsorted_coordinates:
            unsorted_coordinates[name] = unsorted_coordinates[name] / message_count * 100
        #self.coordinates = [(activity, self.coordinates[activity])] for activity in
        #                    sorted(self.coordinates, key=self.coordinates.get, reverse=True)]

        self.coordinates = [(name, unsorted_coordinates[name]) for name in
                             sorted(unsorted_coordinates, key=unsorted_coordinates.get, reverse=True)]

    def __generate_title_week(self):
        """
        - This function generates the title for the Graph
        - This is to follow the naming conventions used in the GraphLine class.
            GraphLine class requires more work to generate its title
        :return: None
        """
        self.title = 'Channel:#{}\nWeekly Percentage'.format(self.channel)

    def __generate_coordinates_week(self):
        """
        - This function acts as a wrapper to format the steps in a readable manner
        :return:
        """
        # Connect to database and fill up self.query_results
        self.__query_results()
        # Calculate each individual's percentage of the total amount of messages
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

        # Close the connection
        client.close()

    def generate_coordinates(self):
        """
        - This function checks the intervals that has been set when creating the object
            and direct the appropriate methods to handle it
        :return:
        """

        # Clears all the coordinates first in case this function is called a second time
        self.coordinates.clear()

        # Case to handle week interval
        if self.interval == 'week':
            self.__generate_title_week()
            self.__generate_coordinates_week()