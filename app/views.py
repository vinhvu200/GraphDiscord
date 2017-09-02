import datetime

import pygal
from flask import render_template
from pymongo import MongoClient

from app import app
from app.scripts import Util

# Getting credentials
f = open('Stuff.txt', 'r')
link = f.readline()
f.close()

mongo_client = MongoClient(link)
db = mongo_client.discord_data
posts = db.messages


@app.route('/')
@app.route('/days')
def test():

    # Current day activities
    timedelta = 0
    interval = 'day'
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_0 = '{} {}'.format(string_day, date)
    activity_graph_0 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage
    activity_graph_percentage_0 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 1
    timedelta = 1
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_1 = '{} {}'.format(string_day, date)
    activity_graph_1 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 1
    activity_graph_percentage_1 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 2
    timedelta = 2
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_2 = '{} {}'.format(string_day, date)
    activity_graph_2 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 2
    activity_graph_percentage_2 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 3
    timedelta = 3
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_3 = '{} {}'.format(string_day, date)
    activity_graph_3 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 3
    activity_graph_percentage_3 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 4
    timedelta = 4
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_4 = '{} {}'.format(string_day, date)
    activity_graph_4 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 4
    activity_graph_percentage_4 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 5
    timedelta = 5
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_5 = '{} {}'.format(string_day, date)
    activity_graph_5 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 5
    activity_graph_percentage_5 = generate_daily_activity_percentage_graph(timedelta)

    # Current day activities. Timedelta 6
    timedelta = 6
    _, _, real_start, _ = Util.get_times(interval, timedelta)
    date = '{} . {} . {}'.format(real_start.month, real_start.day, real_start.year)
    string_day = datetime.datetime.strptime(date, '%m . %d . %Y').strftime('%A')
    date_timedelta_6 = '{} {}'.format(string_day, date)
    activity_graph_6 = generate_daily_activity_graph(timedelta)

    # Current day activities percentage. Timedelta 6
    activity_graph_percentage_6 = generate_daily_activity_percentage_graph(timedelta)

    return render_template("index.html",
                           date_timedelta_0=date_timedelta_0,
                           activity_graph_0=activity_graph_0,
                           activity_graph_percentage_0=activity_graph_percentage_0,
                           date_timedelta_1=date_timedelta_1,
                           activity_graph_1=activity_graph_1,
                           activity_graph_percentage_1=activity_graph_percentage_1,
                           date_timedelta_2=date_timedelta_2,
                           activity_graph_2=activity_graph_2,
                           activity_graph_percentage_2=activity_graph_percentage_2,
                           date_timedelta_3=date_timedelta_3,
                           activity_graph_3=activity_graph_3,
                           activity_graph_percentage_3=activity_graph_percentage_3,
                           date_timedelta_4=date_timedelta_4,
                           activity_graph_4=activity_graph_4,
                           activity_graph_percentage_4=activity_graph_percentage_4,
                           date_timedelta_5=date_timedelta_5,
                           activity_graph_5=activity_graph_5,
                           activity_graph_percentage_5=activity_graph_percentage_5,
                           date_timedelta_6=date_timedelta_6,
                           activity_graph_6=activity_graph_6,
                           activity_graph_percentage_6=activity_graph_percentage_6)


@app.route('/weeks')



def generate_daily_activity_graph(timedelta):
    time = activity_day(posts, timedelta)
    line_chart = pygal.Line()
    line_chart.title = 'Discord Daily Activities by Hours'
    line_chart.x_labels = map(str, range(0, 24))
    line_chart.add('Everyone', time)
    return line_chart.render_data_uri()


def generate_daily_activity_percentage_graph(timedelta):
    activity_percentage = activity_day_percentage(posts, timedelta)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Discord Daily Activity Percentage'
    for name, percentage in activity_percentage:
        pie_chart.add(name, round(percentage, 2))
    return pie_chart.render_data_uri()


def generate_weekly_activity_graph(timedelta):
    pass


def generate_weekly_activity_percentage_graph(timedelta):
    pass


def activity_day(messages_collection, delta):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception as e:
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


def activity_day_percentage(messages_collection, timedelta):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, timedelta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception as e:
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
