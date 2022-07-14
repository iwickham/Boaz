# currently in us
import numpy as np
import html
import time
import pandas as pd
import plotly.express as px
import csv
import requests
import dash
import os
import arcgis
import dash_bootstrap_components as dbc

from tqdm import tqdm
# from imports
from dash import html, dcc, State, Input, Output

# Globally used
apikey = 'Removed for Saftey'
internalend = 0
GResltCount = 0
start_time = time.time()

# address
csv_file = "inputtData.csv"
csv_columns = ['Removed']

# transactions
csv_file2 = "transaction.csv"
trans_csv_columns = ["Removed"]

# constituents
csv_file3 = "constituents.csv"
cons_csv_columns = ["Removed"]
desired_width = 1000

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns', 10)


# Address Functions
def addresscheckcall():
    if not os.path.exists("inputtData.csv"):
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/Addresses?skip=0&take=50'
        req = requests.get(url, headers=header).json()
        GResltCount = req['Total']
        print("Pre Request to set max value: ", req)
        fetchaddresses(GResltCount)
    else:
        if os.path.exists("inputtData.csv"):
            os.remove("inputtData.csv")
            header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
            url = 'https://api.bloomerang.co/v2/Addresses?skip=0&take=50'
            req = requests.get(url, headers=header).json()
            GResltCount = req['Total']
            print("Pre Request to set max value: ", req)
            fetchaddresses(GResltCount)


def fetchaddresses(GResltCount):
    x = 0

    if os.path.exists("inputtData.csv"):
        os.remove("inputtData.csv")

    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

    while x <= GResltCount:
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/Addresses?skip={0}&take={1}'.format(str(x), str(50))
        req = requests.get(url, headers=header).json()

        try:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                for data in req['Results']:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        x = int(x) + 50
        print(req)
        print("--- %s seconds ---" % (time.time() - start_time))


# End

# transaction functions
def transactioncheckcall():
    if not os.path.exists(csv_file2):
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/transactions?skip=0&take=50'
        req = requests.get(url, headers=header).json()
        GResltCount = req['Total']
        print("Pre Request to set max value: ", req)
        fetchtransactions(GResltCount)
    else:
        if os.path.exists(csv_file2):
            os.close(csv_file2)
            os.remove(csv_file2)
            header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
            url = 'https://api.bloomerang.co/v2/transactions?skip=0&take=50'
            req = requests.get(url, headers=header).json()
            GResltCount = req['Total']
            print("Pre Request to set max value: ", req)
            fetchtransactions(GResltCount)


def fetchtransactions(GResltCount):
    x = 0

    if os.path.exists(csv_file2):
        os.remove(csv_file2)

    with open(csv_file2, 'a', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=trans_csv_columns)
        writer.writeheader()

    while x <= GResltCount:
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/transactions?skip={0}&take={1}'.format(str(x), str(50))
        req = requests.get(url, headers=header).json()

        try:
            with open(csv_file2, 'a', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=trans_csv_columns)
                for data in req['Results']:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        x = int(x) + 50
        print(req)
        print("--- %s seconds ---" % (time.time() - start_time))


# End

# constituent functions
def constituentscheckcall():
    if not os.path.exists(csv_file3):
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/constituents?skip=0&take=50'
        req = requests.get(url, headers=header).json()
        GResltCount = req['Total']
        print("Pre Request to set max value: ", req)
        constituent(GResltCount)
    else:
        if os.path.exists(csv_file3):
            os.remove(csv_file3)
            header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
            url = 'https://api.bloomerang.co/v2/constituents?skip=0&take=50'
            req = requests.get(url, headers=header).json()
            GResltCount = req['Total']
            print("Pre Request to set max value: ", req)
            constituent(GResltCount)


def constituent(GResltCount):
    x = 0
    if os.path.exists("constituents.csv"):
        os.remove("constituents.csv")

    with open(csv_file3, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cons_csv_columns)
        writer.writeheader()

    while x <= GResltCount:
        header = ({'Content-Type': 'application/json', 'X-API-KEY': apikey})
        url = 'https://api.bloomerang.co/v2/constituents?skip={0}&take={1}'.format(str(x), str(50))
        req = requests.get(url, headers=header).json()
        print(req)
        try:
            with open(csv_file3, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cons_csv_columns)
                for data in req['Results']:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        x = int(x) + 50
        print(req)
        print("--- %s seconds ---" % (time.time() - start_time))


# End

# data show and clean

# currently rebuilding Geolocation at bottom outside functions
def geolocation():
    # df = pd.read_csv(csv_file, encoding='latin1')
    # df.pop('Note')
    # df = df[df['IsBad'] == True]
    # df['FullAdd'] = df['Street'] + ',' + df['City'] + ',' + df['State']
    # df.to_csv['ge.csv']
    print("hi")


def mondayyear(DMY):
    if os.path.exists('transaction.csv'):
        df = pd.read_csv('transaction.csv')
        df.pop('Designations')
        df.pop('AuditTrail')
        df = df[df.IsRefunded != 'Yes']
        # date value
        header = ['Date', 'Amount']
        df.to_csv('TransDateAmount.csv', columns=header)
        df2 = pd.read_csv('TransDateAmount.csv')

        df2 = df2.groupby('Date').sum()
        df2.drop_duplicates()
        df2.index = pd.to_datetime(df2.index)
        df2
        print(type(df2.index))

        df2.index = pd.to_datetime(df2.index)
        # Create new columns
        df2['year'] = df2.index.year
        df2['month'] = df2.index.month
        df2['day'] = df2.index.day

        df2 = df2.groupby([str(DMY)]).sum()

        print(df2.info)

        fig = px.line(df2, y="Amount", markers=True, title="Total Amount to day: " + (str(df2["Amount"].sum())))
        print("--- %s seconds ---" % (time.time() - start_time))
        return fig
    else:
        transactioncheckcall()

    df = pd.read_csv('transaction.csv')
    df.pop('Designations')
    df.pop('AuditTrail')
    df = df[df.IsRefunded != 'Yes']
    # date value
    header = ['Date', 'Amount']
    df.to_csv('TransDateAmount.csv', columns=header)
    df2 = pd.read_csv('TransDateAmount.csv')

    df2 = df2.groupby('Date').sum()
    df2.drop_duplicates()
    df2.index = pd.to_datetime(df2.index)
    df2
    print(type(df2.index))

    df2.index = pd.to_datetime(df2.index)
    # Create new columns
    df2['year'] = df2.index.year
    df2['month'] = df2.index.month
    df2['day'] = df2.index.day

    df2 = df2.groupby([str(DMY)]).sum()

    print(df2.info)

    fig = px.line(df2, y="Amount", markers=True, title="Total Amount to day: " + (str(df2["Amount"].sum())))
    print("--- %s seconds ---" % (time.time() - start_time))
    return fig


def mergedata():
    dataa = pd.read_csv("constituents.csv", encoding='latin1')
    datab = pd.read_csv("transaction.csv", encoding='latin1')
    datac = pd.read_csv("inputtData.csv", encoding='latin1')

    datab.rename(columns={"Id": "TransId"}, inplace=True)
    datab.rename(columns={"AccountId": "Id"}, inplace=True)

    datac.rename(columns={"Id": "AddId"}, inplace=True)
    datac.rename(columns={"AccountId": "Id"}, inplace=True)

    output = pd.merge(dataa, datab, on="Id")
    df = pd.merge(datac, output, on="Id")
    pd.set_option('display.max_columns', None)

    df['FullAdd'] = df['Street'] + ',' + df['City'] + ',' + df['State']
    df = df[df['Status'] == 'Active']
    df = df[df['IsBad'] == False]

    df.to_csv("allData.csv")


# End

# ------------------
#
# DASH APPLICATION
#
# ------------------
def dashApp():
    app = dash.Dash(
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        # these meta_tags ensure content is scaled correctly on different devices
        # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )
    # we use the Row and Col components to construct the sidebar header
    # it consists of a title, and a toggle, the latter is hidden on large screens
    sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("Boaz Project", className="display-4")),
            dbc.Col(
                [
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "border-color": "rgba(0,0,0,.1)",
                        },
                        id="navbar-toggle",
                    ),
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "border-color": "rgba(0,0,0,.1)",
                        },
                        id="sidebar-toggle",
                    ),
                ],
                # the column containing the toggle will be only as wide as the
                # toggle, resulting in the toggle being right aligned
                width="auto",
                # vertically align the toggle in the center
                align="center",
            ),
        ]
    )

    sidebar = html.Div(
        [
            sidebar_header,
            # we wrap the horizontal rule and short blurb in a div that can be
            # hidden on a small screen
            html.Div(
                [
                    html.Hr(),
                    html.P(
                        "Welcome to Boaz Project Data Analytics",
                        className="lead",
                    ),
                ],
                id="blurb",
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavLink("Home", href="/", active="exact"),
                        dbc.NavLink("Totals", href="/page-1", active="exact"),
                        dbc.NavLink("Geo", href="/page-2", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse",
            ),
        ],
        id="sidebar",
    )

    content = html.Div(id="page-content")

    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

    dropdownsitin = ["Day", "Month", "Year"]

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return
        elif pathname == "/page-1":
            return html.Div(children=[
                # All elements from the top of the page
                html.Div([
                    html.Div([
                        html.H1(children=dropdownsitin[0]),

                        html.Div(children='''
                            '''),

                        dcc.Graph(
                            id='graph1',
                            figure=mondayyear("day")
                        ),
                    ], className='six columns'),
                    html.Div([
                        html.H1(children=dropdownsitin[1]),

                        html.Div(children='''
                            '''),

                        dcc.Graph(
                            id='graph2',
                            figure=mondayyear("month")
                        ),
                    ], className='six columns'),
                ], className='row'),
                # New Div for all elements in the new 'row' of the page
                html.Div([
                    html.H1(children=dropdownsitin[2]),

                    html.Div(children='''
                        '''),

                    dcc.Graph(
                        id='graph3',
                        figure=mondayyear("year")
                    ),
                ], className='row'),
            ])
        elif pathname == "/page-2":
            return html.Div(children=[
                # All elements from the top of the page
                html.Div([
                    html.Div([
                        html.H1(children='GeoMap'),

                        html.Div(children='''
                                        '''),

                        dcc.Graph(
                            id='graph1',
                            figure=geolocation()
                        ),
                    ], className='six columns'),

                ], className='row'),
            ])
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

    # ------------------
    #
    # app call backs
    #
    # ------------------
    @app.callback(
        Output("sidebar", "className"),
        [Input("sidebar-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname == "":
            return "collapsed"
        return ""

    @app.callback(
        Output("collapse", "is_open"),
        [Input("navbar-toggle", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # ------------------
    #
    # Run and where is host
    #
    # ------------------
    if __name__ == "__main__":
        app.run_server(port=8888, debug=True)


# End

df = pd.read_csv('allData.csv', encoding='latin1')
df = df[['Id', 'FirstName', 'LastName', 'Type_y', "FullAdd", 'Amount']]
df.to_csv("SelectData.csv")
df2 = pd.read_csv('SelectData.csv')

total = df2.groupby(['Id', 'FirstName', 'LastName', 'FullAdd']).sum()
total.rename(columns={"Amount": "Total"}, inplace=True)

Max = df2.groupby(['Id', 'FirstName', 'LastName', 'FullAdd']).max()
Max.rename(columns={"Amount": "Max"}, inplace=True)

Min = df2.groupby(['Id', 'FirstName', 'LastName', 'FullAdd']).min()
Min.rename(columns={"Amount": "Min"}, inplace=True)

Median = df2.groupby(['Id', 'FirstName', 'LastName', 'FullAdd']).median()
Median.rename(columns={"Amount": "Median"}, inplace=True)

TMaxmerge = pd.merge(total, Max, on=(['Id', 'FirstName', 'LastName', 'FullAdd']))
TMMinmerge = pd.merge(Min, TMaxmerge, on=(['Id', 'FirstName', 'LastName', 'FullAdd']))
fullMerge = pd.merge(Median, TMMinmerge, on=(['Id', 'FirstName', 'LastName', 'FullAdd']))

print(fullMerge.info)

# start fixing geocode/new service
geo = arcgis.geocoding.batch_geocode(address=fullMerge["FullAdd"])


# Pie
# fig2 = px.sunburst(df, path=['Type', 'EngagementScore'])
# fig.show()
# fig2.show()

print("--- %s seconds ---" % (time.time() - start_time), apikey)
# for printing how long it
# took for the application to run,
# also wanted to check the userin apikey (removed function)
