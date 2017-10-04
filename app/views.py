import threading, time

from flask import render_template
from app import app
from app.model import Graph


@app.route('/SkypeCurrent')
def skypeCurrent():

    # Variables to set the graph
    graph1_interval = 'day'
    graph2_interval = 'week'
    graph3_interval = 'week_percent'
    channel = 'skype'
    timedelta = 0

    # Generate day graph
    graph1 = Graph.Graph(graph1_interval, channel, timedelta)
    graph1.generate_graph()

    # Generate week graph
    graph2 = Graph.Graph(graph2_interval, channel, timedelta)
    graph2.generate_graph()

    # Generate week percent graph
    graph3 = Graph.Graph(graph3_interval, channel, timedelta)
    graph3.generate_graph()

    return render_template("SkypeCurrent.html",
                           day_graph=graph1.rendered_graph,
                           week_graph=graph2.rendered_graph,
                           week_percent_graph=graph3.rendered_graph)


#@app.route('/')
@app.route('/GeneralCurrent')
def generalCurrent():
    # Variables to set the graph
    graph1_interval = 'day'
    graph2_interval = 'week'
    graph3_interval = 'week_percent'
    channel = 'general'
    timedelta = 0

    # Generate day graph
    graph1 = Graph.Graph(graph1_interval, channel, timedelta)
    graph1.generate_graph()

    # Generate week graph
    graph2 = Graph.Graph(graph2_interval, channel, timedelta)
    graph2.generate_graph()

    # Generate week percent graph
    graph3 = Graph.Graph(graph3_interval, channel, timedelta)
    graph3.generate_graph()

    return render_template("GeneralCurrent.html",
                           day_graph=graph1.rendered_graph,
                           week_graph=graph2.rendered_graph,
                           week_percent_graph=graph3.rendered_graph)


#@app.route('/')
@app.route('/SkypeDays')
def skype_day():

    graph_interval = 'day'
    channel = 'skype'
    graphs = []

    for timedelta in range(2):
        graph = Graph.Graph(graph_interval, channel, timedelta)
        graph.generate_graph()
        graphs.append(graph)

    return render_template("SkypeDays.html",
                           day_graph_0=graphs[0].rendered_graph,
                           day_graph_1=graphs[1].rendered_graph)


#@app.route('/')
@app.route('/SkypeWeeks')
def skype_weeks():

    graph_interval = 'week'
    channel = 'skype'
    graphs = []

    for timedelta in range(1):
        graph = Graph.Graph(graph_interval, channel, timedelta)
        graph.generate_graph()
        graphs.append(graph)

    return render_template("SkypeWeeks.html",
                           week_graph_0=graphs[0].rendered_graph)


@app.route('/')
@app.route('/SkypeDistribution')
def skype_distribution():

    graph_type = 'week_percent'
    channel = 'skype'
    graphs = []

    for timedelta in range(2):
        graph = Graph.Graph(graph_type, channel, timedelta)
        graph.generate_graph()
        graphs.append(graph)

    return render_template("SkypeDistribution.html",
                           week_percent_graph_0=graphs[0].rendered_graph,
                           week_percent_graph_1=graphs[1].rendered_graph)


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html")
