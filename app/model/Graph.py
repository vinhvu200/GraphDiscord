import datetime

class Graph:

    def __init__(self):
        self.type = None
        self.channel = None
        self.graph = None

    def generate(self):
        pass

    def calculate_activity_day(self):
        pass

    def calculate_activity_week(self):
        pass

    @staticmethod
    def __get_times(self, interval, timedelta):
        if interval == 'day':

            # Calculate utc and real end time
            utc_end = datetime.datetime.utcnow()
            real_end = utc_end - datetime.timedelta(hours=7)

            # Calculate utc and real start time
            utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
            real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

            if timedelta > 0:
                # Adjust utc time range with delta
                utc_end = utc_start - datetime.timedelta(days=timedelta - 1)
                utc_start = utc_start - datetime.timedelta(days=timedelta)

                # Adjust real time range with delta
                real_end = real_start - datetime.timedelta(days=timedelta - 1)
                real_start = real_start - datetime.timedelta(days=timedelta)

        elif interval == 'week':

            Days = {'Monday': 0,
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

            utc_start = utc_end - datetime.timedelta(days=Days[string_day], hours=real_end.hour,
                                                     minutes=real_end.minute)
            real_start = real_end - datetime.timedelta(days=Days[string_day], hours=real_end.hour,
                                                       minutes=real_end.minute)

            # Adjust utc time range with delta
            utc_end = utc_start - datetime.timedelta(days=(timedelta - 1) * 7)
            utc_start = utc_start - datetime.timedelta(days=timedelta * 7)

            # Adjust real time range with delta
            real_end = real_start - datetime.timedelta(days=(timedelta - 1) * 7)
            real_start = real_start - datetime.timedelta(days=timedelta * 7)

        else:
            utc_start = utc_end = real_start = real_end = -1

        return utc_start, utc_end, real_start, real_end

    def __calculate_daily_activities(self, query_results, real_end_hour):
        pass