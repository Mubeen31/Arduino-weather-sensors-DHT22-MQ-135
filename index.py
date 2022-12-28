from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your pages
from apps import outside, inside, data

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),

    dbc.Navbar(children=[
        dbc.Container([
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
            )]
        ),
        dbc.NavItem(dbc.NavLink('Outside', href='/apps/outside', class_name='nav_item_color'),
                    class_name='nav_item'),
        dbc.NavItem(dbc.NavLink('Inside', href='/apps/inside', class_name='nav_item_color'),
                    class_name='nav_item'),
        dbc.NavItem(dbc.NavLink('Data', href='/apps/data', class_name='nav_item_color'),
                    class_name='nav_item')

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


if __name__ == '__main__':
    app.run_server(debug=True
                   )
