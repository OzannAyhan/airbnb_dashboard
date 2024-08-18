from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
import config
from src.layout import create_layout
from src.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[BOOTSTRAP, "https://use.fontawesome.com/releases/v5.8.1/css/all.css"])
app.config.suppress_callback_exceptions = True

app.layout = create_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=config.DEBUG)