import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])

server = app.server
