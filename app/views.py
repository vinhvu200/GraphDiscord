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
@app.route('/index')
def index():

    interval = 'day'

    # Lists to hold information for each Carousel slide
    dates = []
    activity_graphs = []
    activity_graphs_percentages = []

    # Generate graphs for each day in the last week
    for timedelta in range(0, 7):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = generate_daily_activity_graph(timedelta)
        activity_graph_percentage = generate_daily_activity_percentage_graph(timedelta)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("index.html",
                           date_timedelta_0=dates[0],
                           activity_graph_0=activity_graphs[0],
                           activity_graph_percentage_0=activity_graphs_percentages[0],
                           date_timedelta_1=dates[1],
                           activity_graph_1=activity_graphs[1],
                           activity_graph_percentage_1=activity_graphs_percentages[1],
                           date_timedelta_2=dates[2],
                           activity_graph_2=activity_graphs[2],
                           activity_graph_percentage_2=activity_graphs_percentages[2],
                           date_timedelta_3=dates[3],
                           activity_graph_3=activity_graphs[3],
                           activity_graph_percentage_3=activity_graphs_percentages[3],
                           date_timedelta_4=dates[4],
                           activity_graph_4=activity_graphs[4],
                           activity_graph_percentage_4=activity_graphs_percentages[4],
                           date_timedelta_5=dates[5],
                           activity_graph_5=activity_graphs[5],
                           activity_graph_percentage_5=activity_graphs_percentages[5],
                           date_timedelta_6=dates[6],
                           activity_graph_6=activity_graphs[6],
                           activity_graph_percentage_6=activity_graphs_percentages[6])


#@app.route('/')
@app.route('/test')
@app.route('/week')
def test():

    interval = 'week'
    dates = []
    activity_graphs = []
    activity_graphs_percentages = []
    for timedelta in range(0, 3):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = generate_weekly_activity_graph(timedelta)
        activity_graph_percentage = generate_weekly_activity_percentage_graph(timedelta)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("weeks.html",
                           date_timedelta_0=dates[0],
                           activity_graph_0=activity_graphs[0],
                           activity_graph_percentage_0=activity_graphs_percentages[0],
                           date_timedelta_1=dates[1],
                           activity_graph_1=activity_graphs[1],
                           activity_graph_percentage_1=activity_graphs_percentages[1],
                           date_timedelta_2=dates[2],
                           activity_graph_2=activity_graphs[2],
                           activity_graph_percentage_2=activity_graphs_percentages[2])


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

    days, message_counts = activity_week(posts, timedelta)
    line_chart = pygal.Line()
    line_chart.title = 'Discord Weekly activity'
    line_chart.x_labels = map(str, days)
    line_chart.add('Everyone', message_counts)
    return line_chart.render_data_uri()


def generate_weekly_activity_percentage_graph(timedelta):
    activities = activity_week_percentage(posts, timedelta)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Percentages of User Weekly Activity'
    for name, percentage in activities:
        pie_chart.add(name, round(percentage, 2))
    return pie_chart.render_data_uri()


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


def activity_week(messages_collection, delta):
    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
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


def activity_week_percentage(messages_collection, delta):
    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    activities = Util.calculate_weekly_activities_percentage(query_results)

    message = 'Activities between {}.{}.{} -- {}.{}.{}:\n' \
              '----------------------------\n'.format(real_start.month, real_start.day,
                                                      real_start.year, real_end.month,
                                                      real_end.day, real_end.year)
    for name, percentage in activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))

    return activities
