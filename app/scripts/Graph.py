import pygal
import datetime
import collections

from app.scripts import Util


def generate_daily_activity_graph(posts, timedelta, channel):
    time = activity_day(posts, timedelta, channel)
    line_chart = pygal.Line()
    line_chart.title = 'Discord Daily Activities by Hours'
    line_chart.x_labels = map(str, range(0, 24))
    line_chart.add('Everyone', time)
    return line_chart.render_data_uri()


def generate_daily_activity_percentage_graph(posts, timedelta, channel):
    activity_percentage = activity_day_percentage(posts, timedelta, channel)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Discord Daily Activity Percentage'
    for name, percentage in activity_percentage:
        pie_chart.add(name, round(percentage, 2))
    return pie_chart.render_data_uri()


def generate_weekly_activity_graph(posts, timedelta, channel):

    days, message_counts = activity_week(posts, timedelta, channel)
    line_chart = pygal.Line()
    line_chart.title = 'Discord Weekly activity'
    line_chart.x_labels = map(str, days)
    line_chart.add('Everyone', message_counts)
    return line_chart.render_data_uri()


def generate_weekly_activity_graph2(posts, channel):

    days = collections.OrderedDict()
    days['Monday'] = 0
    days['Tuesday'] = 1
    days['Wednesday'] = 2
    days['Thursday'] = 3
    days['Friday'] = 4
    days['Saturday'] = 5
    days['Sunday'] = 6

    line_chart = pygal.Line()
    line_chart.x_labels = map(str, range(24))
    line_chart.title = 'Discord Weekly Activity'

    _, string_day = activity_day2(posts, 0, channel)
    completed_days = days[string_day]

    days = collections.OrderedDict()

    for timedelta_day in range(completed_days, -1, -1):
        time, string_day = activity_day2(posts, timedelta_day, channel)
        days[string_day] = time

    for day in days:
        line_chart.add(day, days[day])

    return line_chart.render_data_uri()


def generate_weekly_activity_percentage_graph(posts, timedelta, channel):
    activities = activity_week_percentage(posts, timedelta, channel)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Weekly User Percentage Activity'
    for name, percentage in activities:
        pie_chart.add(name, round(percentage, 2))
    return pie_chart.render_data_uri()


def activity_day(messages_collection, delta, channel):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': channel})
    except Exception as e:
        print('inside: activity day')
        print(e)
        return None

    # If delta is 0, then you have to search for when the time is 'not yet recorded'
    # Otherwise, all time will have been accounted for
    if delta == 0:
        activities_by_hours = Util.calculate_daily_activities(query_results, real_end.hour)
    else:
        activities_by_hours = Util.calculate_daily_activities(query_results, None)

    times = []
    for x in range(0, 24):
        times.append(activities_by_hours[x])

    return times


def activity_day2(messages_collection, delta, channel):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)
    date = '{} / {} / {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m / %d / %Y').strftime('%A')

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': channel})
    except Exception as e:
        print('inside: activity day')
        print(e)
        return None

    # If delta is 0, then you have to search for when the time is 'not yet recorded'
    # Otherwise, all time will have been accounted for
    if delta == 0:
        activities_by_hours = Util.calculate_daily_activities(query_results, real_end.hour)
    else:
        activities_by_hours = Util.calculate_daily_activities(query_results, None)

    times = []
    for x in range(0, 24):
        times.append(activities_by_hours[x])

    return times, string_day


def activity_day_percentage(messages_collection, timedelta, channel):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, timedelta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': channel})
    except Exception as e:
        print('inside: activity day percentage')
        print(e)
        return None

    # Calculate message count and activities with query_results
    activities = Util.calculate_daily_activities_percentage(query_results)

    # Format message
    message = 'Activities for {} . {} . {}:\n' \
              '----------------------------\n'.format(real_start.month,
                                                      real_start.day,
                                                      real_start.year)
    for name, percentage in activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))

    return activities


def activity_week(messages_collection, delta, channel):
    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': channel})
    except Exception as e:
        print(e)
        return 'Could not retrieve from database. Vinh failed you'

    # Get weekly activities
    activities = Util.calculate_weekly_activities(query_results)

    # Format Message
    message = 'Message count: {}.{}.{} -- {}.{}.{}\n' \
              '------------------------------\n'.format(real_start.month, real_start.day,
                                                        real_start.year, real_end.month,
                                                        real_end.day, real_end.year)

    days = []
    message_count = []
    for day in activities:
        message += '{} -- {}\n'.format(day, activities[day])
        days.append(day)
        message_count.append(activities[day])

    return days, message_count


def activity_week_percentage(messages_collection, delta, channel):
    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': channel})
    except Exception as e:
        print('inside activity week percentage')
        print(e)
        return 'Could not retrieve from database. Vinh failed you'

    activities = Util.calculate_weekly_activities_percentage(query_results)

    message = 'Activities between {}.{}.{} -- {}.{}.{}:\n' \
              '----------------------------\n'.format(real_start.month, real_start.day,
                                                      real_start.year, real_end.month,
                                                      real_end.day, real_end.year)
    for name, percentage in activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))

    return activities

