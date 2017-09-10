import datetime

import pygal
from flask import render_template
from pymongo import MongoClient

from app import app
from app.scripts import Util
from app.scripts import Graph

# Getting credentials
f = open('Stuff.txt', 'r')
link = f.readline()
f.close()

mongo_client = MongoClient(link)
db = mongo_client.discord_data
posts = db.messages

@app.route('/GeneralDays')
@app.route('/')
def generalDays():
    interval = 'day'
    channel = 'general'

    # Lists to hold information for each Carousel slide
    dates = []
    activity_graphs = []
    activity_graphs_percentages = []

    # Generate graphs for each day in the last week
    for timedelta in range(0, 7):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = Graph.generate_daily_activity_graph(posts, timedelta, channel)
        activity_graph_percentage = Graph.generate_daily_activity_percentage_graph(posts, timedelta, channel)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("GeneralDays.html",
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


@app.route('/GeneralWeeks')
def generalWeeks():
    interval = 'week'
    channel = 'general'

    dates = []
    activity_graphs = []
    activity_graphs_percentages = []
    for timedelta in range(0, 3):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = Graph.generate_weekly_activity_graph(posts, timedelta, channel)
        activity_graph_percentage = Graph.generate_weekly_activity_percentage_graph(posts, timedelta, channel)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("GeneralWeeks.html",
                           date_timedelta_0=dates[0],
                           activity_graph_0=activity_graphs[0],
                           activity_graph_percentage_0=activity_graphs_percentages[0],
                           date_timedelta_1=dates[1],
                           activity_graph_1=activity_graphs[1],
                           activity_graph_percentage_1=activity_graphs_percentages[1],
                           date_timedelta_2=dates[2],
                           activity_graph_2=activity_graphs[2],
                           activity_graph_percentage_2=activity_graphs_percentages[2])


@app.route('/SkypeDays')
@app.route('/index')
def skypeDays():

    interval = 'day'
    channel = 'skype'

    # Lists to hold information for each Carousel slide
    dates = []
    activity_graphs = []
    activity_graphs_percentages = []

    # Generate graphs for each day in the last week
    for timedelta in range(0, 7):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = Graph.generate_daily_activity_graph(posts, timedelta, channel)
        activity_graph_percentage = Graph.generate_daily_activity_percentage_graph(posts, timedelta, channel)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("SkypeDays.html",
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


@app.route('/SkypeWeeks')
def skypeWeeks():

    interval = 'week'
    channel = 'skype'
    dates = []
    activity_graphs = []
    activity_graphs_percentages = []
    for timedelta in range(0, 3):
        date = Util.get_date_timedelta(interval, timedelta)
        activity_graph = Graph.generate_weekly_activity_graph(posts, timedelta, channel)
        activity_graph_percentage = Graph.generate_weekly_activity_percentage_graph(posts, timedelta, channel)

        dates.append(date)
        activity_graphs.append(activity_graph)
        activity_graphs_percentages.append(activity_graph_percentage)

    return render_template("SkypeWeeks.html",
                           date_timedelta_0=dates[0],
                           activity_graph_0=activity_graphs[0],
                           activity_graph_percentage_0=activity_graphs_percentages[0],
                           date_timedelta_1=dates[1],
                           activity_graph_1=activity_graphs[1],
                           activity_graph_percentage_1=activity_graphs_percentages[1],
                           date_timedelta_2=dates[2],
                           activity_graph_2=activity_graphs[2],
                           activity_graph_percentage_2=activity_graphs_percentages[2])


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html")