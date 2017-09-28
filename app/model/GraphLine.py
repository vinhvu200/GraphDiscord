import datetime
from database import get_db
from collections import OrderedDict


class GraphLine:

    def __init__(self, interval, channel, timedelta):
        self.title = None
        self.coordinates = []
        self.interval = interval
        self.timedelta = timedelta
        self.query_results = None
        self.current_hour = None
        self.channel = channel

    def calculate_weekly_activities(self):

        activities = OrderedDict()
        activities['Monday'] = None
        activities['Tuesday'] = None
        activities['Wednesday'] = None
        activities['Thursday'] = None
        activities['Friday'] = None
        activities['Saturday'] = None
        activities['Sunday'] = None

        for query in self.query_results:

            time = query['time']
            time = time - datetime.timedelta(hours=7)
            day = '{} {} {}'.format(time.month, time.day, time.year)
            string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

            if activities[string_day] is None:
                activities[string_day] = 1
            else:
                activities[string_day] += 1

        return activities

    def __calculate_daily_activities(self):
        messages = [0] * 24
        for query in self.query_results:

            if query['time'].hour - 7 >= 0:
                adjusted = query['time'].hour - 7
            else:
                adjusted = 24 + (query['time'].hour - 7)

            messages[adjusted] += 1

        if self.current_hour is not None:
            for x in range(self.current_hour + 1, 24):
                messages[x] = None

        return messages

    def __generate_coordinates_day(self):
        client, db, collection = get_db()

        # Get appropriate time range
        utc_start, utc_end, real_start, real_end = self.__get_time_range()

        # Attempt to query by dates
        try:
            self.query_results = collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': self.channel})
        except Exception as e:
            print(e)
            return None

        # If delta is 0, then you have to search for when the time is 'not yet recorded'
        # Otherwise, all time will have been accounted for
        if self.timedelta == 0:
            activities_by_hours = self.__calculate_daily_activities()
        else:
            activities_by_hours = self.__calculate_daily_activities()

        for x in range(0, 24):
            self.coordinates.append(activities_by_hours[x])

        client.close()

    def __generate_coordinates_week(self):

        client, db, collection = get_db()

        # Get appropriate time range
        utc_start, utc_end, real_start, real_end = self.__get_time_range()

        # Attempt to query by dates
        try:
            self.query_results = collection.find({'time': {'$gte': utc_start, '$lt': utc_end},
                                                  'channel': self.channel})
        except Exception as e:
            print(e)
            return 'Could not retrieve from database. Vinh failed you'

        # Get weekly activities
        activities = self.calculate_weekly_activities()

        #days = []
        #message_count = []
        for day in activities:
            #days.append(day)
            #message_count.append(activities[day])
            self.coordinates.append(activities[day])

        client.close()

    def __generate_title_day(self):
        # Get the day in which this data is for ('Monday', 'Tuesday'... etc)
        _, _, real_start, _ = self.__get_time_range()

        date = '{} / {} / {}'.format(real_start.month, real_start.day, real_start.year)
        self.title = datetime.datetime.strptime(date, '%m / %d / %Y').strftime('%A')

    def __generate_title_week(self):

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

        if self.interval == 'day':

            # Calculate utc and real end time
            utc_end = datetime.datetime.utcnow()
            real_end = utc_end - datetime.timedelta(hours=7)

            # Calculate utc and real start time
            utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
            real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

            if self.timedelta > 0:
                # Adjust utc time range with delta
                utc_end = utc_start - datetime.timedelta(days=self.timedelta - 1)
                utc_start = utc_start - datetime.timedelta(days=self.timedelta)

                # Adjust real time range with delta
                real_end = real_start - datetime.timedelta(days=self.timedelta - 1)
                real_start = real_start - datetime.timedelta(days=self.timedelta)

        elif self.interval == 'week':

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

            day = '{} {} {}'.format(real_end.month, real_end.day, real_end.year)
            string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

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

        else:
            utc_start = utc_end = real_start = real_end = -1

        return utc_start, utc_end, real_start, real_end

    def generate_coordinates(self):

        if self.interval == 'day':
            self.__generate_title_day()
            self.__generate_coordinates_day()
        elif self.interval == 'week':
            self.__generate_title_week()
            self.__generate_coordinates_week()
