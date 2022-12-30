from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from app import app
from google.oauth2 import service_account
import pandas_gbq as pd1
import pandas as pd
from dash import dash_table

# credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
# project_id = 'weatherdata1'
# df3_sql = f"""SELECT
#              *
#              FROM
#              `weatherdata1.WeatherSensorsData1.SensorsData1`
#              ORDER BY
#              DateTime DESC LIMIT 1
#              """
# df4 = pd1.read_gbq(df3_sql, project_id=project_id, dialect='standard', credentials=credentials)
df4 = pd.read_csv('data.csv')
df4['DateTime'] = pd.to_datetime(df4['DateTime'])
df4['Date'] = df4['DateTime'].dt.date
df4['Date'] = pd.to_datetime(df4['Date'])
df4['Hour'] = pd.to_datetime(df4['DateTime']).dt.hour

layout = html.Div([

    html.Div([
        dcc.Interval(id='update_value3',
                     interval=1 * 1000,
                     n_intervals=0),
    ]),

    html.Div([
        html.Div(id='total_rows',
                 className='header_text1')
    ], className='header_card1'),

    html.Div([
        html.Div([dash_table.DataTable(id='my_datatable',
                                       columns=[{"name": i, "id": i} for i in df4.columns],
                                       page_size=13,
                                       sort_action="native",
                                       sort_mode="multi",
                                       virtualization=True,
                                       style_cell={'textAlign': 'left',
                                                   'min-width': '100px',
                                                   'backgroundColor': 'rgba(255, 255, 255, 0)',
                                                   'minWidth': 180,
                                                   'maxWidth': 180,
                                                   'width': 180},
                                       style_header={
                                           'backgroundColor': 'black',
                                           'fontWeight': 'bold',
                                           'font': 'Lato, sans-serif',
                                           'color': 'orange',
                                           'border': '1px solid white',
                                       },
                                       style_data={'textOverflow': 'hidden',
                                                   'color': 'black',
                                                   'fontWeight': 'bold',
                                                   'font': 'Lato, sans-serif'},
                                       fixed_rows={'headers': True},
                                       )
                  ], className='bg_table')
    ], className='bg_container')
])


@app.callback(Output('total_rows', 'children'),
              [Input('update_value3', 'n_intervals')])
def update_value(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        # credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        # project_id = 'weatherdata1'
        # df_sql = f"""SELECT
        #          *
        #          FROM
        #          `weatherdata1.WeatherSensorsData1.SensorsData1`
        #          ORDER BY
        #          DateTime ASC
        #          """
        # df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        df = pd.read_csv('data.csv')
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
        df['Date'] = df['DateTime'].dt.date
        df['Hour'] = pd.to_datetime(df['DateTime']).dt.hour
        unique_date = df['Date'].unique()
        filter_today_date = len(df[df['Date'] == unique_date[-1]])
        filter_total_rows = len(df['Date'])

    return [
        html.Div([
            html.Div([
                html.Div('Total rows in the database are',
                         className='description'),
                html.Div('{0:,.0f}'.format(filter_total_rows) + '.',
                         className='database_total_rows'
                         ),
            ], className='make_rows'),
            html.Div([
                html.Div('Today total rows have been added in the database',
                         className='description'),
                html.Div('{0:,.0f}'.format(filter_today_date) + '.',
                         className='database_total_rows'
                         ),
            ], className='make_rows'),
        ], className='make_rows')

    ]


@app.callback(Output('my_datatable', 'data'),
              [Input('update_value3', 'n_intervals')])
def display_table(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        # credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        # project_id = 'weatherdata1'
        # df_sql = f"""SELECT
        #          *
        #          FROM
        #          `weatherdata1.WeatherSensorsData1.SensorsData1`
        #          ORDER BY
        #          DateTime DESC
        #          """
        # df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        df = pd.read_csv('data.csv')
        df.sort_values(by='DateTime', ascending=False, inplace=True)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
        df['Date'] = df['DateTime'].dt.date
        df['Hour'] = pd.to_datetime(df['DateTime']).dt.hour
        return df.to_dict('records')
