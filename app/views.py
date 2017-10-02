import threading, time

from flask import render_template
from app import app
from app.scripts import Util, Graph
from database import get_db
from app.model import GraphLine
from app.model import Graph as Graphz

general_day_dates = []
general_day_activity_graphs = []
general_day_activity_graphs_percentages = []
general_day_lock = threading.Lock()

general_week_dates = []
general_week_activity_graphs = []
general_week_activity_graphs_percentages = []
general_week_lock = threading.Lock()

skype_day_dates = []
skype_day_activity_graphs = []
skype_day_activity_graphs_percentages = []
skype_day_lock = threading.Lock()

skype_week_dates = []
skype_week_activity_graphs = []
skype_week_activity_graphs_percentages = []
skype_week_lock = threading.Lock()


def update_general_day(lock):
    interval = 'day'
    channel = 'general'

    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                client, db, messages = get_db()
                del general_day_dates[:]
                del general_day_activity_graphs[:]
                del general_day_activity_graphs_percentages[:]
                for timedelta in range(0, 7):
                    date = Util.get_date_timedelta(interval, timedelta)
                    activity_graph = Graph.generate_daily_activity_graph(messages, timedelta, channel)
                    activity_graph_percentage = Graph.generate_daily_activity_percentage_graph(messages, timedelta, channel)

                    general_day_dates.append(date)
                    general_day_activity_graphs.append(activity_graph)
                    general_day_activity_graphs_percentages.append(activity_graph_percentage)
        finally:
            if have_it:
                client.close()
                lock.release()

        if have_it:
            time.sleep(600)
        else:
            print('did not get lock and retrying')
            time.sleep(2)


def update_general_week(lock):
    interval = 'week'
    channel = 'general'
    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                client, db, messages = get_db()
                del general_week_dates[:]
                del general_week_activity_graphs[:]
                del general_week_activity_graphs_percentages[:]
                for timedelta in range(0, 3):
                    date = Util.get_date_timedelta(interval, timedelta)
                    activity_graph = Graph.generate_weekly_activity_graph(messages, timedelta, channel)
                    activity_graph_percentage = \
                        Graph.generate_weekly_activity_percentage_graph(messages, timedelta, channel)

                    general_week_dates.append(date)
                    general_week_activity_graphs.append(activity_graph)
                    general_week_activity_graphs_percentages.append(activity_graph_percentage)
        finally:
            if have_it:
                client.close()
                lock.release()

        if have_it:
            time.sleep(600)
        else:
            time.sleep(2)


def update_skype_day(lock):
    interval = 'day'
    channel = 'skype'
    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                client, db, messages = get_db()
                del skype_day_dates[:]
                del skype_day_activity_graphs[:]
                del skype_day_activity_graphs_percentages[:]

                # Generate graphs for each day in the last week
                for timedelta in range(0, 7):
                    date = Util.get_date_timedelta(interval, timedelta)
                    activity_graph = Graph.generate_daily_activity_graph(messages, timedelta, channel)
                    activity_graph_percentage = Graph.generate_daily_activity_percentage_graph(messages, timedelta,
                                                                                               channel)

                    skype_day_dates.append(date)
                    skype_day_activity_graphs.append(activity_graph)
                    skype_day_activity_graphs_percentages.append(activity_graph_percentage)
        finally:
            if have_it:
                client.close()
                lock.release()

        if have_it:
            time.sleep(600)
        else:
            time.sleep(2)


def update_skype_week(lock):
    interval = 'week'
    channel = 'skype'

    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                client, db, messages = get_db()
                del skype_week_dates[:]
                del skype_week_activity_graphs[:]
                del skype_week_activity_graphs_percentages[:]

                for timedelta in range(0, 3):
                    date = Util.get_date_timedelta(interval, timedelta)
                    activity_graph = Graph.generate_weekly_activity_graph(messages, timedelta, channel)
                    activity_graph_percentage = Graph.generate_weekly_activity_percentage_graph(messages, timedelta, channel)

                    skype_week_dates.append(date)
                    skype_week_activity_graphs.append(activity_graph)
                    skype_week_activity_graphs_percentages.append(activity_graph_percentage)
        finally:
            if have_it:
                client.close()
                lock.release()

        if have_it:
            time.sleep(600)
        else:
            time.sleep(2)


general_day_thread = threading.Thread(
    target=update_general_day,
    args=(general_day_lock,),
    name='general_day_thread'
)
general_day_thread.start()

general_week_thread = threading.Thread(
    target=update_general_week,
    args=(general_week_lock,),
    name='general_week_thread'
)
general_week_thread.start()

skype_day_thread = threading.Thread(
    target=update_skype_day,
    args=(skype_day_lock,),
    name='skype_day_thread'
)
skype_day_thread.start()

skype_week_thread = threading.Thread(
    target=update_skype_week,
    args=(skype_week_lock,),
    name='skype_week_thread'
)
skype_week_thread.start()


@app.route('/GeneralDays')
#@app.route('/')
def general_days():

    have_it = general_day_lock.acquire(0)
    while not have_it:
        have_it = general_day_lock.acquire(0)
        time.sleep(2)

    template = render_template("GeneralDays.html",
                               date_timedelta_0=general_day_dates[0],
                               activity_graph_0=general_day_activity_graphs[0],
                               activity_graph_percentage_0=general_day_activity_graphs_percentages[0],
                               date_timedelta_1=general_day_dates[1],
                               activity_graph_1=general_day_activity_graphs[1],
                               activity_graph_percentage_1=general_day_activity_graphs_percentages[1],
                               date_timedelta_2=general_day_dates[2],
                               activity_graph_2=general_day_activity_graphs[2],
                               activity_graph_percentage_2=general_day_activity_graphs_percentages[2],
                               date_timedelta_3=general_day_dates[3],
                               activity_graph_3=general_day_activity_graphs[3],
                               activity_graph_percentage_3=general_day_activity_graphs_percentages[3],
                               date_timedelta_4=general_day_dates[4],
                               activity_graph_4=general_day_activity_graphs[4],
                               activity_graph_percentage_4=general_day_activity_graphs_percentages[4],
                               date_timedelta_5=general_day_dates[5],
                               activity_graph_5=general_day_activity_graphs[5],
                               activity_graph_percentage_5=general_day_activity_graphs_percentages[5],
                               date_timedelta_6=general_day_dates[6],
                               activity_graph_6=general_day_activity_graphs[6],
                               activity_graph_percentage_6=general_day_activity_graphs_percentages[6])
    general_day_lock.release()

    return template


@app.route('/GeneralWeeks')
def general_weeks():
    have_it = general_week_lock.acquire(0)
    while not have_it:
        have_it = general_week_lock.acquire(0)
        time.sleep(2)

    template = render_template("GeneralWeeks.html",
                               date_timedelta_0=general_week_dates[0],
                               activity_graph_0=general_week_activity_graphs[0],
                               activity_graph_percentage_0=general_week_activity_graphs_percentages[0],
                               date_timedelta_1=general_week_dates[1],
                               activity_graph_1=general_week_activity_graphs[1],
                               activity_graph_percentage_1=general_week_activity_graphs_percentages[1],
                               date_timedelta_2=general_week_dates[2],
                               activity_graph_2=general_week_activity_graphs[2],
                               activity_graph_percentage_2=general_week_activity_graphs_percentages[2])
    general_week_lock.release()
    return template


@app.route('/SkypeDays')
@app.route('/index')
def skype_days():
    have_it = skype_day_lock.acquire(0)
    while not have_it:
        have_it = skype_day_lock.acquire(0)
        time.sleep(2)

    template = render_template("SkypeDays.html",
                               date_timedelta_0=skype_day_dates[0],
                               activity_graph_0=skype_day_activity_graphs[0],
                               activity_graph_percentage_0=skype_day_activity_graphs_percentages[0],
                               date_timedelta_1=skype_day_dates[1],
                               activity_graph_1=skype_day_activity_graphs[1],
                               activity_graph_percentage_1=skype_day_activity_graphs_percentages[1],
                               date_timedelta_2=skype_day_dates[2],
                               activity_graph_2=skype_day_activity_graphs[2],
                               activity_graph_percentage_2=skype_day_activity_graphs_percentages[2],
                               date_timedelta_3=skype_day_dates[3],
                               activity_graph_3=skype_day_activity_graphs[3],
                               activity_graph_percentage_3=skype_day_activity_graphs_percentages[3],
                               date_timedelta_4=skype_day_dates[4],
                               activity_graph_4=skype_day_activity_graphs[4],
                               activity_graph_percentage_4=skype_day_activity_graphs_percentages[4],
                               date_timedelta_5=skype_day_dates[5],
                               activity_graph_5=skype_day_activity_graphs[5],
                               activity_graph_percentage_5=skype_day_activity_graphs_percentages[5],
                               date_timedelta_6=skype_day_dates[6],
                               activity_graph_6=skype_day_activity_graphs[6],
                               activity_graph_percentage_6=skype_day_activity_graphs_percentages[6])
    skype_day_lock.release()
    return template


@app.route('/SkypeWeeks')
def skype_weeks():
    have_it = skype_week_lock.acquire(0)
    while not have_it:
        have_it = skype_week_lock.acquire(0)
        time.sleep(2)

    template = render_template("SkypeWeeks.html",
                               date_timedelta_0=skype_week_dates[0],
                               activity_graph_0=skype_week_activity_graphs[0],
                               activity_graph_percentage_0=skype_week_activity_graphs_percentages[0],
                               date_timedelta_1=skype_week_dates[1],
                               activity_graph_1=skype_week_activity_graphs[1],
                               activity_graph_percentage_1=skype_week_activity_graphs_percentages[1],
                               date_timedelta_2=skype_week_dates[2],
                               activity_graph_2=skype_week_activity_graphs[2],
                               activity_graph_percentage_2=skype_week_activity_graphs_percentages[2])
    skype_week_lock.release()
    return template


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html")


@app.route('/test')
def test():
    channel = 'general'
    timedelta = 0
    client, db, messages = get_db()

    activity_graph_hour = Graph.generate_activity_graph_hour(messages, channel)
    activity_graph_day = Graph.generate_activity_graph_day(messages, channel)
    activity_graph_percentage = \
        Graph.generate_weekly_activity_percentage_graph(messages, timedelta, channel)

    client.close()
    return render_template("test.html",
                           activity_graph_hour=activity_graph_hour,
                           activity_graph_day=activity_graph_day,
                           activity_percentage_graph=activity_graph_percentage)


@app.route('/')
@app.route('/test2')
def test2():

    graph = Graphz.Graph('day', 'skype', 0)
    graph.generate_graph()

    channel = 'skype'
    timedelta = 0
    client, db, messages = get_db()

    activity_graph_hour = Graph.generate_activity_graph_hour(messages, channel)
    activity_graph_day = Graph.generate_activity_graph_day(messages, channel)

    activity_graph_percentage = \
        Graph.generate_weekly_activity_percentage_graph(messages, timedelta, channel)

    client.close()
    return render_template("test2.html",
                           activity_graph_hour=graph.rendered_graph,
                           activity_graph_day=activity_graph_day,
                           activity_percentage_graph=activity_graph_percentage)