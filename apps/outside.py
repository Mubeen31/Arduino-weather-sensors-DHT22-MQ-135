from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import app
import pandas as pd
import csv

layout = html.Div([

    html.Div([
        dcc.Interval(id='update_value1',
                     interval=1 * 5000,
                     n_intervals=0),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.Div(
                    'Arduino DHT22 and MQ-135 sensors measure the temperature, humidity and level of CO2 in the air of '
                    'area ',
                    className='description'),
                html.Div('Walsall, England. ', className='location_name')
            ], className='text_row')
        ], className='header_text')
    ], className='header_card'),

    html.Div([
        html.Div([
            html.Div(id='value1',
                     className='card_size1'),
            html.Div(id='value2',
                     className='card_size2'),
            html.Div(id='value3',
                     className='card_size3')
        ], className='value_cards_column'),
        html.Div([
            dcc.Graph(id='line_chart',
                      config={'displayModeBar': False}),
        ], className='chart')
    ], className='numeric_values_container')
])


@app.callback(Output('value1', 'children'),
              [Input('update_value1', 'n_intervals')])
def update_value(n_intervals):
    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df3 = pd.read_csv('data1.csv', names=header)
    df3.drop_duplicates(keep=False, inplace=True)
    get_temp = df3['OutsideTemperature'].tail(1).iloc[0]

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


@app.callback(Output('value2', 'children'),
              [Input('update_value1', 'n_intervals')])
def update_value(n_intervals):
    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df3 = pd.read_csv('data1.csv', names=header)
    df3.drop_duplicates(keep=False, inplace=True)
    get_humidity = df3['OutsideHumidity'].tail(1).iloc[0]

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


@app.callback(Output('value3', 'children'),
              [Input('update_value1', 'n_intervals')])
def update_value(n_intervals):
    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df3 = pd.read_csv('data1.csv', names=header)
    df3.drop_duplicates(keep=False, inplace=True)
    get_co2 = df3['OutsideCO2'].tail(1).iloc[0]

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


@app.callback(Output('line_chart', 'figure'),
              [Input('update_value1', 'n_intervals')])
def line_chart_values(n_intervals):
    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df3 = pd.read_csv('data1.csv', names=header)
    df3['DateTime'] = pd.to_datetime(df3['DateTime'])
    df3['Date'] = df3['DateTime'].dt.date
    df3['Date'] = pd.to_datetime(df3['Date'])
    df3['Hour'] = pd.to_datetime(df3['DateTime']).dt.hour
    df3.drop_duplicates(keep=False, inplace=True)
    unique_date = df3['Date'].unique()
    filter_today_date = df3[df3['Date'] == unique_date[-1]][['Date', 'Hour', 'OutsideTemperature']]
    today_hourly_values = filter_today_date.groupby(['Date', 'Hour'])['OutsideTemperature'].mean().reset_index()

    return {
        'data': [go.Scatter(
            x=today_hourly_values['Hour'],
            y=today_hourly_values['OutsideTemperature'],
            mode='markers+lines',
            line=dict(width=3, color='#CA23D5'),
            marker=dict(size=7, symbol='circle', color='#CA23D5',
                        line=dict(color='#CA23D5', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + today_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + today_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in today_hourly_values['OutsideTemperature']] + '<br>'
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