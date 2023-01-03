from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1
import csv

# Connect to main app.py file
from app import app
from app import server

# Connect to your pages
from apps import outside, inside, data

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),

    dcc.Interval(id='update_value',
                 interval=1 * 11000,
                 n_intervals=0),

    dbc.Navbar(children=[
        html.Div([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src=app.get_asset_url('sensor.png'), height='30px')),
                    dbc.Col(dbc.NavbarBrand('Arduino Weather Sensors', className='ms-2')),
                ],
                    align='center',
                    className='g-0',
                ),
                href='/apps/outside',
                style={'textDecoration': 'none'},
            ),

            html.Div([
                html.Div('Sensors Location: Walsall, England',
                         className='location'),

                dbc.Spinner(html.Div(id='date',
                                     className='date_id'))
            ], className='location_date_time')
        ], className='nav_title'),

        dbc.Nav([dbc.NavItem(dbc.NavLink('Outside', href='/apps/outside',
                                         active='exact',
                                         style={'color': 'white'})
                             ),
                 dbc.NavItem(dbc.NavLink('Inside', href='/apps/inside',
                                         active='exact',
                                         style={'color': 'white'})
                             ),
                 dbc.NavItem(dbc.NavLink('Data', href='/apps/data',
                                         active='exact',
                                         style={'color': 'white'})
                             )

                 ],
                pills=True,
                class_name='nav_items'
                ),

    ],
        color='dark',
        dark=True,
    ),

    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/outside':
        return outside.layout
    elif pathname == '/apps/inside':
        return inside.layout
    elif pathname == '/apps/data':
        return data.layout
    else:
        return outside.layout


@app.callback(Output('date', 'children'),
              [Input('update_value', 'n_intervals')])
def update_confirmed(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT *
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
    df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df1 = df.tail(1)
    df2 = df1.values.tolist()[0]
    with open('data1.csv', 'a', newline='\n') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(df2)

    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df3 = pd.read_csv('data1.csv', names=header)
    get_date = df3['DateTime'].tail(1).iloc[0]

    return [
        html.Div('Last Date Update Time: ' + get_date,
                 className='date_format')
    ]


if __name__ == '__main__':
    app.run_server(debug=True
                   )
