import datetime
from database import get_db
from collections import OrderedDict


class GraphLine:
    """
    In order to utilize this class, interval, channel, and timedelta MUST
    be initialized. Otherwise, there would be no point
    """

    def __init__(self, interval, channel, timedelta):
        self.title = None
        self.coordinates = []
        self.interval = interval
        self.timedelta = timedelta
        self.query_results = None
        self.channel = channel

    def __calculate_daily_activities(self, current_hour):
        """
        This function looks through the query results (which should already be defined)
        and uses an array to store the message_count. Each index represents the hour.

        :return: array containing message_count
        """

        # Creates array to count messages by hours
        message_count = [0] * 24

        # Look through all the query results
        for query in self.query_results:

            # Adjusted utc time to pacific time
            if query['time'].hour - 7 >= 0:
                adjusted = query['time'].hour - 7
            else:
                adjusted = 24 + (query['time'].hour - 7)

            # Increment message count according to the hour
            message_count[adjusted] += 1

        # Set everything past the current hour to None those points shouldn't be plotted
        if current_hour is not None:
            for x in range(current_hour + 1, 24):
                message_count[x] = None

        # return the array
        return message_count

    def __calculate_weekly_activities(self):
        """
        This function uses an Ordered Dictionary to map the days
        to its message_count

        :return: Ordered Dictionary mapping days to message_count
        """

        # Initialize the Ordered Dictionary to None so we don't plot points that don't exist
        activities = OrderedDict()
        activities['Monday'] = None
        activities['Tuesday'] = None
        activities['Wednesday'] = None
        activities['Thursday'] = None
        activities['Friday'] = None
        activities['Saturday'] = None
        activities['Sunday'] = None

        # Check all results in query_results
        for result in self.query_results:

            # Adjust the time
            time = result['time']
            time = time - datetime.timedelta(hours=7)

            # Get the string_day
            day = '{} {} {}'.format(time.month, time.day, time.year)
            string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

            # Increment message_count in OrderedDict
            if activities[string_day] is None:
                activities[string_day] = 1
            else:
                activities[string_day] += 1

        # return OrderedDict
        return activities

    def __generate_coordinates_day(self):
        """
        This function generates the coordinates for the day interval and stores it in the
        coordinates list

        :return: Nothing
        """

        # Open client to access database
        client, db, collection = get_db()

        # Get appropriate time range
        utc_start, utc_end, real_start, real_end = self.__get_time_range()

        # Attempt to query using dates, and channels
        try:
            self.query_results = collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': self.channel})
        except Exception as e:
            print(e)
            return None

        # If delta is 0, then you have to search for when the time is 'not yet recorded'
        # Otherwise, all time will have been accounted for
        if self.timedelta == 0:
            activities_by_hours = self.__calculate_daily_activities(real_end.hour)
        else:
            activities_by_hours = self.__calculate_daily_activities(None)

        # Append all activities into coordinates
        for x in range(0, 24):
            self.coordinates.append(activities_by_hours[x])

        # Close client
        client.close()

    def __generate_coordinates_week(self):
        """
        This function generates the coordinates for the week interval and stores it in
        the coordinates list

        :return: Nothing
        """

        # Open client to access database
        client, db, collection = get_db()

        # Get appropriate time range
        utc_start, utc_end, real_start, real_end = self.__get_time_range()

        # Attempt to query using dates, and channels
        try:
            self.query_results = collection.find({'time': {'$gte': utc_start, '$lt': utc_end},
                                                  'channel': self.channel})
        except Exception as e:
            print(e)
            return 'Could not retrieve from database. Vinh failed you'

        # Get weekly activities
        activities = self.__calculate_weekly_activities()

        for day in activities:
            self.coordinates.append(activities[day])

        client.close()

    def __generate_title_day(self):
        """
        This function generates the title of the line for day interval and stores it in
        the self.title variable

        :return: Nothing
        """
        # Get the day in which this data is for ('Monday', 'Tuesday'... etc)
        _, _, real_start, _ = self.__get_time_range()

        date = '{} / {} / {}'.format(real_start.month, real_start.day, real_start.year)
        self.title = datetime.datetime.strptime(date, '%m / %d / %Y').strftime('%A')

    def __generate_title_week(self):
        """
        This function generates the title of the line for week interval and stores it
        in the self.title variable

        :return: Nothing
        """

        # Title is set up to 4 weeks back depending on timedelta
        if self.timedelta == 0:
            self.title = 'Today'
        elif self.timedelta == 1:
            self.title = 'Last week'
        elif self.timedelta == 2:
            self.title = 'Two weeks ago'
        elif self.timedelta == 3:
            self.title = 'Three weeks ago'
        else:
            self.title = 'None'

    def __get_time_range(self):
        """
        This function determines the start and end time (both utc and real) to be used for
        the query. It is determined using self.interval and self.timedelta

        :return: utc and real time range
        """

        # Case for day interval
        if self.interval == 'day':

            # Calculate utc and real end time
            utc_end = datetime.datetime.utcnow()
            real_end = utc_end - datetime.timedelta(hours=7)

            # Calculate utc and real start time
            utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
            real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

            # Handles whether timedelta is bigger than 0
            if self.timedelta > 0:
                # Adjust utc time range with delta
                utc_end = utc_start - datetime.timedelta(days=self.timedelta - 1)
                utc_start = utc_start - datetime.timedelta(days=self.timedelta)

                # Adjust real time range with delta
                real_end = real_start - datetime.timedelta(days=self.timedelta - 1)
                real_start = real_start - datetime.timedelta(days=self.timedelta)

        # Case for week interval (Weeks begin on a Monday)
        elif self.interval == 'week':

            # Determines how many days to subtract by for the current week (Week begins on Monday)
            days = {'Monday': 0,
                    'Tuesday': 1,
                    'Wednesday': 2,
                    'Thursday': 3,
                    'Friday': 4,
                    'Saturday': 5,
                    'Sunday': 6}

            # Calculate utc and real end time
            utc_end = datetime.datetime.utcnow()
            real_end = utc_end - datetime.timedelta(hours=7)

            # Get the string_day (Monday, Tuesday... etc)
            day = '{} {} {}'.format(real_end.month, real_end.day, real_end.year)
            string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

            # Adjust the current utc/real time to have it start on a Monday
            utc_start = utc_end - datetime.timedelta(days=days[string_day], hours=real_end.hour,
                                                     minutes=real_end.minute)
            real_start = real_end - datetime.timedelta(days=days[string_day], hours=real_end.hour,
                                                       minutes=real_end.minute)

            # Adjust utc time range with delta
            utc_end = utc_start - datetime.timedelta(days=(self.timedelta - 1) * 7)
            utc_start = utc_start - datetime.timedelta(days=self.timedelta * 7)

            # Adjust real time range with delta
            real_end = real_start - datetime.timedelta(days=(self.timedelta - 1) * 7)
            real_start = real_start - datetime.timedelta(days=self.timedelta * 7)

        # This case should never happen
        else:
            utc_start = utc_end = real_start = real_end = -1

        # Returns utc and real time
        return utc_start, utc_end, real_start, real_end

    def generate_coordinates(self):
        """
        This function generates the title and coordinates for the graph depending on its interval set.
        timedelta MUST have been initiated in order for this to work properly

        :return: Nothing
        """

        # Delete list of coordinates first before appending them
        del self.coordinates[:]

        # Case where interval is day
        if self.interval == 'day':
            self.__generate_title_day()
            self.__generate_coordinates_day()
        # Case where interval is week
        elif self.interval == 'week':
            self.__generate_title_week()
            self.__generate_coordinates_week()
