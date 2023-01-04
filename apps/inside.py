from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from app import app
from google.oauth2 import service_account
import pandas_gbq as pd1
import pandas as pd

layout = html.Div([

    html.Div([
        dcc.Interval(id='update_value2',
                     interval=1 * 11000,
                     n_intervals=0),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.Div(
                    'Arduino DHT22 and MQ-135 sensors measure the temperature, humidity and level of '
                    'CO2 in the air ',
                    className='description'),
                html.Div('inside room. ', className='location_name')
            ], className='text_row')
        ], className='header_text')
    ], className='header_card'),

    html.Div([
        html.Div([
            html.Div(id='value4',
                     className='card_size1'),
            html.Div(id='value5',
                     className='card_size2'),
            html.Div(id='value6',
                     className='card_size3')
        ], className='value_cards_column'),
        html.Div([
            dcc.Graph(id='line_chart1',
                      config={'displayModeBar': False}),
        ], className='chart')
    ], className='numeric_values_container')
])


@app.callback(Output('value4', 'children'),
              [Input('update_value2', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT InsideTemperature
                                 FROM
                                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                                 ORDER BY
                                 DateTime DESC LIMIT 1
                                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    get_temp = df3['InsideTemperature'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Temperature (°C)', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('thermometer.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.1f}'.format(get_temp),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


@app.callback(Output('value5', 'children'),
              [Input('update_value2', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT InsideHumidity
                                 FROM
                                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                                 ORDER BY
                                 DateTime DESC LIMIT 1
                                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    get_humidity = df3['InsideHumidity'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Humidity (%)', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('humidity.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.1f}'.format(get_humidity),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


@app.callback(Output('value6', 'children'),
              [Input('update_value2', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT InsideCO2
                                 FROM
                                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                                 ORDER BY
                                 DateTime DESC LIMIT 1
                                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    get_co2 = df3['InsideCO2'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Air Quality (PPM)', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('air-quality.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.0f}'.format(get_co2),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value2', 'n_intervals')])
def line_chart_values(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT DateTime, InsideTemperature
                                 FROM
                                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                                 ORDER BY
                                 DateTime ASC
                                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3['DateTime'] = pd.to_datetime(df3['DateTime'])
    df3['Date'] = df3['DateTime'].dt.date
    df3['Date'] = pd.to_datetime(df3['Date'])
    df3['Hour'] = pd.to_datetime(df3['DateTime']).dt.hour
    unique_date = df3['Date'].unique()
    filter_today_date = df3[df3['Date'] == unique_date[-1]][['Date', 'Hour', 'InsideTemperature']]
    today_hourly_values = filter_today_date.groupby(['Date', 'Hour'])['InsideTemperature'].mean().reset_index()

    return {
        'data': [go.Scatter(
            x=today_hourly_values['Hour'],
            y=today_hourly_values['InsideTemperature'],
            mode='markers+lines',
            line=dict(width=3, color='#CA23D5'),
            marker=dict(size=7, symbol='circle', color='#CA23D5',
                        line=dict(color='#CA23D5', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + today_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + today_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in today_hourly_values['InsideTemperature']] + '<br>'
        )],

        'layout': go.Layout(
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={
                'text': 'Today Temperature (°C)',
                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#ffbf00',
                'size': 17},
            hovermode='x unified',
            margin=dict(t=50, r=40),
            xaxis=dict(
                tick0=0,
                dtick=1,
                title='<b>Hours</b>',
                color='#ffffff',
                showline=True,
                showgrid=False,
                linecolor='#ffffff',
                linewidth=1,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='#ffffff')

            ),

            yaxis=dict(
                title='<b>Temperature (°C)</b>',
                color='#ffffff',
                zeroline=False,
                showline=True,
                showgrid=False,
                linecolor='#ffffff',
                linewidth=1,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='#ffffff')

            ),
            font=dict(
                family="sans-serif",
                size=12,
                color='#ffffff')

        )

    }