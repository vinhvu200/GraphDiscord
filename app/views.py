from flask import render_template
from app import app
from pymongo import MongoClient
import datetime
import pygal
from collections import OrderedDict

# Getting credentials
f = open('Stuff.txt', 'r')
link = f.readline()
f.close()

client = MongoClient(link)
db = client.discord_data
posts = db.messages

#@app.route('/')
@app.route('/index')
def graphs():

    time = detail_day()
    line_chart = pygal.Bar()
    line_chart.title = 'Discord Details'
    line_chart.x_labels = map(str, range(0, 24))
    line_chart.add('Everyone', time)
    graph_data = line_chart.render_data_uri()

    counts, days = detail_week()
    line_chart = pygal.Line()
    line_chart.title = 'Discord Weekly activity'
    line_chart.x_labels = map(str, days)
    line_chart.add('Everyone', counts)
    graph_data2 = line_chart.render_data_uri()

    activities = activity_day()
    pie_chart = pygal.Pie()
    pie_chart.title = 'Percentages of User Daily Activity'
    for name, percentage in activities:
        pie_chart.add(name, round(percentage, 2))
    graph_data3 = pie_chart.render_data_uri()

    activities2 = activity_week()
    pie_chart2 = pygal.Pie()
    pie_chart2.title = 'Percentages of User Weekly Activity'
    for name, percentage in activities2:
        pie_chart2.add(name, round(percentage, 2))
    graph_data4 = pie_chart2.render_data_uri()

    return render_template("graph.html", graph_data=graph_data,
                           graph_data2=graph_data2,
                           graph_data3=graph_data3,
                           graph_data4=graph_data4)

@app.route('/')
@app.route('/test')
def test():
    time = detail_day()
    line_chart = pygal.Bar()
    line_chart.title = 'Discord Details'
    line_chart.x_labels = map(str, range(0, 24))
    line_chart.add('Everyone', time)
    graph_data = line_chart.render_data_uri()

    activities = activity_day()
    pie_chart = pygal.Pie()
    pie_chart.title = 'Percentages of User Daily Activity'
    for name, percentage in activities:
        pie_chart.add(name, round(percentage, 2))
    graph_data2 = pie_chart.render_data_uri()

    counts, days = detail_week()
    line_chart = pygal.Line()
    line_chart.title = 'Discord Weekly activity'
    line_chart.x_labels = map(str, days)
    line_chart.add('Everyone', counts)
    graph_data3 = line_chart.render_data_uri()

    activities2 = activity_week()
    pie_chart2 = pygal.Pie()
    pie_chart2.title = 'Percentages of User Weekly Activity'
    for name, percentage in activities2:
        pie_chart2.add(name, round(percentage, 2))
    graph_data4 = pie_chart2.render_data_uri()

    return render_template("index.html", graph_data=graph_data,
                           graph_data2=graph_data2,
                           graph_data3=graph_data3,
                           graph_data4=graph_data4)

def detail_week():

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)

    activities = OrderedDict()

    try:
        query_results = posts.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    for query in query_results:

        time = query['time']
        time = time - datetime.timedelta(hours=7)
        day = '{} {} {}'.format(time.month, time.day, time.year)
        string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

        if string_day in activities:
            activities[string_day] += 1
        else:
            activities[string_day] = 1

    message = 'Message count: {}.{}.{} -- {}.{}.{}\n' \
              '------------------------------\n'.format(real_start.month, real_start.day,
                                                        real_start.year, real_end.month,
                                                        real_end.day, real_end.year)

    message_count = []
    time = []
    for day in activities:
        message += '{} -- {}\n'.format(day, activities[day])
        message_count.append(activities[day])
        time.append(day)

    return message_count, time

def detail_day():

    time = []
    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)
    utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

    messages = [0] * (real_end.hour + 1)
    try:
        query_results = posts.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    message_count = 0
    for query in query_results:

        if query['time'].hour - 7 >= 0:
            adjusted = query['time'].hour - 7
        else:
            adjusted = 24 - query['time'].hour - 7

        messages[adjusted] += 1
        message_count += 1

    message = 'Message count per hour for {} . {} . {}\n'.format(real_start.month,
                                                                 real_start.day,
                                                                 real_start.year)

    for x in range(0, real_end.hour+1):
        message += '\t{}:00   ---   {}\n'.format(x, messages[x])
        time.append(messages[x])

    return time

def activity_day():

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)
    utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

    try:
        query_results = posts.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    message_count = 0
    activities = dict()

    for query in query_results:
        full_name = query['author'].split('#')
        name = full_name[0]
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1
        message_count += 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    message = 'Activities for {} . {} . {}:\n' \
              '----------------------------\n'.format(real_start.month,
                                                      real_start.day,
                                                      real_start.year)

    names = []
    percentages = []
    for name, percentage in sorted_activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))

    return sorted_activities


def activity_week():

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)

    try:
        query_results = posts.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    message_count = 0
    activities = dict()
    for query in query_results:
        message_count += 1
        full_name = query['author'].split('#')
        name = full_name[0]
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    message = 'Activities between {}.{}.{} -- {}.{}.{}:\n' \
              '----------------------------\n'.format(real_start.month, real_start.day,
                                                      real_start.year, real_end.month,
                                                      real_end.day, real_end.year)
    for name, percentage in sorted_activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))
    return sorted_activities