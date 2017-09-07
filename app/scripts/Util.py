import datetime
from collections import OrderedDict


def calculate_daily_activities(query_results, max_hour):
    messages = [0] * 24
    for query in query_results:

        if query['time'].hour - 7 >= 0:
            adjusted = query['time'].hour - 7
        else:
            adjusted = 24 + (query['time'].hour - 7)

        messages[adjusted] += 1

    if max_hour is not None:
        for x in range(max_hour + 1, 24):
            messages[x] = None

    return messages


def calculate_daily_activities_percentage(query_results):

    message_count = 0
    activities = dict()

    for query in query_results:
        message_count += 1
        name = query['author'].split('#')[0]
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    return sorted_activities


def calculate_weekly_activities(query_results):

    activities = OrderedDict()
    activities['Monday'] = None
    activities['Tuesday'] = None
    activities['Wednesday'] = None
    activities['Thursday'] = None
    activities['Friday'] = None
    activities['Saturday'] = None
    activities['Sunday'] = None

    for query in query_results:

        time = query['time']
        time = time - datetime.timedelta(hours=7)
        day = '{} {} {}'.format(time.month, time.day, time.year)
        string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

        if activities[string_day] is None:
            activities[string_day] = 1
        else:
            activities[string_day] += 1

    return activities


def calculate_weekly_activities_percentage(query_results):

    message_count = 0
    activities = dict()
    for query in query_results:
        message_count += 1
        name = query['author'].split('#')[0]
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    return sorted_activities


def get_date_timedelta(interval, timedelta):

    if interval == 'day':
        _, _, real_start, _ = get_times(interval, timedelta)
        date = '{} / {} / {}'.format(real_start.month, real_start.day, real_start.year)
        string_day = datetime.datetime.strptime(date, '%m / %d / %Y').strftime('%A')
        format_date = '{} {}'.format(string_day, date)
        return format_date
    elif interval == 'week':
        _, _, real_start, real_end = get_times(interval, timedelta)
        date = 'Between: {} / {} / {}  -  {} / {} / {}'.format(real_start.month,
                                                                 real_start.day,
                                                                 real_start.year,
                                                                 real_end.month,
                                                                 real_end.day,
                                                                 real_end.year)
        return date

    return None


def get_times(interval, delta):

    if interval == 'day':

        # Calculate utc and real end time
        utc_end = datetime.datetime.utcnow()
        real_end = utc_end - datetime.timedelta(hours=7)

        # Calculate utc and real start time
        utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
        real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

        if delta > 0:
            # Adjust utc time range with delta
            utc_end = utc_start - datetime.timedelta(days=delta - 1)
            utc_start = utc_start - datetime.timedelta(days=delta)

            # Adjust real time range with delta
            real_end = real_start - datetime.timedelta(days=delta - 1)
            real_start = real_start - datetime.timedelta(days=delta)

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

        utc_start = utc_end - datetime.timedelta(days=Days[string_day], hours=real_end.hour, minutes=real_end.minute)
        real_start = real_end - datetime.timedelta(days=Days[string_day], hours=real_end.hour, minutes=real_end.minute)

        # Adjust utc time range with delta
        utc_end = utc_start - datetime.timedelta(days=(delta - 1) * 7)
        utc_start = utc_start - datetime.timedelta(days=delta * 7)

        # Adjust real time range with delta
        real_end = real_start - datetime.timedelta(days=(delta - 1) * 7)
        real_start = real_start - datetime.timedelta(days=delta * 7)

    else:
        utc_start = utc_end = real_start = real_end = -1

    return utc_start, utc_end, real_start, real_end
