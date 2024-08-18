from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils import get_city_options, get_unique_dates
import config

def create_layout():
    city_options = get_city_options(config.CITY_PATHS)
    unique_dates = get_unique_dates(config.CITY_PATHS)
    date_marks = {i: date.strftime('%Y-%m') for i, date in enumerate(sorted(unique_dates))}

    if len(date_marks) > 2:
        last_key = max(date_marks.keys())
        date_marks[last_key - 1] += " (Forecasted)"
        date_marks[last_key] += " (Forecasted)"

    return html.Div([
        # Navbar
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            # Column for logo and title
                            dbc.Col(html.Img(src='/assets/airbnb_logo.png', height="50px"), width="auto"),
                            dbc.Col(dbc.NavbarBrand("Airbnb Dashboard", className="ml-2", style={"font-size": "30px", "font-weight": "bold", "color": "white"})),
                        ],
                        align="center",  # Center content horizontally
                        className="g-0",  # Remove gaps between columns
                    ),
                    dbc.Row(
                        [
                            # Column for "Select City" label
                            dbc.Col(html.Div("Select City:", style={'fontSize': '22px', 'fontWeight': '580', 'color': 'white', 'textAlign': 'left'})),
                            # Column for dropdown menu
                            dbc.Col(
                                dcc.Dropdown(
                                    id='city-dropdown',
                                    options=city_options,
                                    value='Madrid, Spain',
                                    style={'width': '200px', 'margin': '10px auto', 'borderRadius': '10px', 'padding': '1px', 'fontSize': '17px', 'textAlign': 'left'},
                                    clearable=True,
                                    searchable=True
                                ),
                                width={"size": "auto"}  # Adjust width as needed
                            ),
                        ],
                        align="center",  # Center the entire row horizontally
                        className="g-0",  # Remove gaps between columns
                    ),
                ],
                fluid=True,  # Use full width of the container
            ),
            color=config.COLORS['primary'],
            dark=True,
            className="mb-4",
            style={"padding": "15px 20px"}
        ),

        # City selection section
        html.Div(
            [
                html.H2("SELECT MONTH", style={'fontSize': '19px', 'fontWeight': '580', 'textAlign': 'center', 'color': '#7F7F7F'}),
                dcc.Slider(
                    id='month-slider',
                    min=0,
                    max=len(date_marks) - 1,
                    marks=date_marks,
                    value=0,
                    step=1,
                    className='slider-style'
                ),
                html.Div(id='map-container', style={'transition': 'transform 1s', 'width': '80%', 'margin': '0 auto', 'display': 'flex', 'justify-content': 'center', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'}),
            ],
            style={'padding': '10px', 'backgroundColor': config.COLORS['background']}
        ),

        # Store to hold the clicked neighborhood value
        dcc.Store(id='clicked-neighborhood'),

        # Modal for Top 10 Listings
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(
                        "Neighbourhood Insights",
                        style={'fontSize': '24px', 'fontWeight': 'bold', 'color': 'white'}
                    ),
                    style={'backgroundColor': '#FF5A5F'}  # Change this to your desired background color
                ),
                dbc.ModalBody(
                    [
                        # Buttons to switch between plots
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Price Over Time", id='price-over-time', n_clicks=0, className='mr-2', style={'backgroundColor': '#FFFFFF','color': '#FF5A5F','border': '1px solid #FF5A5F','outline': 'none','boxShadow': 'none'}),
                                dbc.Button("Rating Over Time", id='rating-over-time', n_clicks=0, style={'backgroundColor': '#FF5A5F','color': '#FFFFFF','border': '1px solid #FFFFFF','outline': 'none','boxShadow': 'none'})
                            ], width=12, style={'textAlign': 'center', 'marginBottom': '20px'}),
                        ]),
                        # Scatter Plot Section
                        html.Div([
                            html.H4("Price Over Time", id='plot-title', style={'fontSize': '18px', 'marginTop': '20px', 'textAlign': 'center', 'color': config.COLORS['text']}),
                            dcc.Dropdown(
                                id='neighborhood-dropdown',
                                style={'width': '50%', 'margin': '10px auto', 'borderRadius': '10px', 'padding': '1px', 'fontSize': '15px'},
                                clearable=False,
                                searchable=True
                            ),
                            dcc.Graph(id='scatter-plot'),
                        ], style={'padding': '20px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px', 'marginTop': '20px'}),
                        
                        
                        # Most Frequent Amenities - Bar Graph Section
                        html.Div([
                        html.H4("Most Frequent Amenities", style={'fontSize': '18px', 'marginTop': '20px', 'textAlign': 'center', 'color': config.COLORS['text']}),
                        dcc.Graph(id='Amenities')
                        ], style={'padding': '20px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px', 'marginTop': '20px'}),
     
                        
                        dbc.Row([
                            dbc.Col([
                                html.H4("Sort Table By", style={'fontSize': '18px', 'marginTop': '10px', 'textAlign': 'center', 'color': config.COLORS['text']}),
                                dcc.Dropdown(
                                    id='sort-dropdown',
                                    style={'width': '100%', 'margin': '10px auto', 'borderRadius': '10px', 'padding': '1px', 'fontSize': '15px'},
                                    clearable=False,
                                    searchable=False
                                ),
                            ], width=4),
                            dbc.Col([
                                html.H4("Additional Columns", style={'fontSize': '18px', 'marginTop': '10px', 'textAlign': 'center', 'color': config.COLORS['text']}),
                                dcc.Dropdown(
                                    id='columns-dropdown',
                                    multi=True,
                                    style={'width': '100%', 'margin': '10px auto', 'borderRadius': '10px', 'padding': '1px', 'fontSize': '15px'}
                                ),
                            ], width=4),
                            dbc.Col([
                                html.H4("Order", style={'fontSize': '18px', 'marginTop': '10px', 'textAlign': 'center', 'color': config.COLORS['text']}),
                                html.Div(
                                    children=[
                                        dbc.Button("Ascending", id='order-asc', n_clicks=0, className='mr-2', style={'backgroundColor': '#FFFFFF','color': '#FF5A5F','border': '1px solid #FF5A5F','outline': 'none','boxShadow': 'none'}),
                                        dbc.Button("Descending", id='order-desc', n_clicks=0, style={'backgroundColor': '#FF5A5F','color': '#FFFFFF','border': '1px solid #FFFFFF','outline': 'none','boxShadow': 'none'})
                                    ],
                                    style={'width': '100%', 'textAlign': 'center'}
                                ),
                            ], width=4),
                        ], style={'margin': '20px 0'}),

           
                        html.Div(id='table-container', style={'padding': '20px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'})
                    ]
                ),
            ],
            id="modal",
            size="xl",  # Increase size to "xl" for better visibility
            is_open=False,
        ),
    ], style={'fontFamily': 'Arial, sans-serif', 'padding': '0px', 'backgroundColor': config.COLORS['background']})