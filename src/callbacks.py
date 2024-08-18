from dash.dependencies import Input, Output, State
from dash import html
import pandas as pd
from src.utils import update_map, get_unique_dates, generate_table, get_sort_options, get_column_options, get_neighborhood_options, parse_top_amenities
import plotly.graph_objs as go
from src.data_loader import listings_data, neighborhood_stats, neighborhoods_geojson
import config

unique_dates = get_unique_dates(config.CITY_PATHS)
date_marks = {i: date.strftime('%Y-%m') for i, date in enumerate(sorted(unique_dates))}

def register_callbacks(app):
    @app.callback(
        Output('table-container', 'children'),
        [Input('city-dropdown', 'value'), Input('month-slider', 'value'), Input('sort-dropdown', 'value'), Input('columns-dropdown', 'value'), Input('order-asc', 'n_clicks'), Input('order-desc', 'n_clicks'), Input('neighborhood-dropdown', 'value')]
    )
    def update_table(selected_city, selected_date_index, sort_by, selected_columns, n_clicks_asc, n_clicks_desc, selected_neighborhood):
        if selected_city not in listings_data:
            return html.Div("Invalid city selected")
        
        selected_month = int(date_marks[selected_date_index].split('-')[1])
        listings_filtered = listings_data[selected_city][(listings_data[selected_city]['month'] == selected_month) & (listings_data[selected_city]['neighbourhood_cleansed'] == selected_neighborhood)]

        if sort_by is None:
            sort_by = 'review_scores_rating'
        
        if selected_columns is None:
            selected_columns = []

        columns_to_display = config.DEFAULT_COLUMNS + selected_columns
        columns_to_display = list(dict.fromkeys(columns_to_display))

        order = 'asc' if n_clicks_asc > n_clicks_desc else 'desc'

        table_listings = listings_filtered.sort_values(by=sort_by, ascending=(order == 'asc'))
        table_listings = table_listings[columns_to_display]
        return generate_table(table_listings)

    @app.callback(
        Output('sort-dropdown', 'options'),
        [Input('city-dropdown', 'value')]
    )
    def update_sort_options(selected_city):
        return get_sort_options(listings_data, selected_city)

    @app.callback(
        Output('columns-dropdown', 'options'),
        [Input('city-dropdown', 'value')]
    )
    def update_column_options(selected_city):
        if selected_city in listings_data:
            available_columns = listings_data[selected_city].columns
            additional_columns = [col for col in config.ADDITIONAL_COLUMNS_LIST if col in available_columns]
            return [{'label': config.COLUMN_DISPLAY_NAMES.get(col, col), 'value': col} for col in additional_columns]
        return []

    @app.callback(
        Output('map-container', 'children'),
        [Input('city-dropdown', 'value'), Input('month-slider', 'value')]
    )
    def update_map_callback(selected_city, selected_date_index):
        # Extract the month part, remove any non-numeric characters
        selected_month_str = date_marks[selected_date_index].split('-')[1]
        selected_month = int(''.join(filter(str.isdigit, selected_month_str)))

        # Determine if the selected month is a forecasted month
        is_forecasted = selected_month > 6 and '2024' in date_marks[selected_date_index]
        
        return update_map(selected_city, selected_month, is_forecasted, config.CITY_PATHS, neighborhoods_geojson, neighborhood_stats)

    @app.callback(
        Output('neighborhood-dropdown', 'value'),
        Input('clicked-neighborhood', 'data'),
    )
    def update_neighborhood_dropdown(clicked_neighborhood):
        return clicked_neighborhood

    @app.callback(
        Output("modal", "is_open"),
        Output('clicked-neighborhood', 'data'),
        [Input('map', 'clickData')],
        [State("modal", "is_open")],
    )
    def toggle_modal(clickData, is_open):
        if clickData:
            neighborhood = clickData['points'][0]['location']
            return not is_open, neighborhood
        return is_open, None

    @app.callback(
        Output('scatter-plot', 'figure'),
        Output('plot-title', 'children'),
        [Input('city-dropdown', 'value'), Input('neighborhood-dropdown', 'value'), Input('price-over-time', 'n_clicks'), Input('rating-over-time', 'n_clicks')]
    )
    def update_scatter_plot(selected_city, selected_neighborhood, n_clicks_price, n_clicks_rating):
        if selected_city not in listings_data:
            return go.Figure(), ""

        listings_filtered = listings_data[selected_city][listings_data[selected_city]['neighbourhood_cleansed'] == selected_neighborhood]

        if n_clicks_rating > n_clicks_price:
            listings_aggregated = listings_filtered.groupby('date').agg(
                mean_rating=('review_scores_rating', 'mean')
            ).reset_index()

            # Identify the last two months
            forecast_start_index = -2  # Start of forecasted months

            fig = go.Figure()

            # Add trace for all data points including the connection to the forecasted months
            fig.add_trace(go.Scatter(
                x=listings_aggregated['date'],
                y=listings_aggregated['mean_rating'],
                mode='lines',  # Connect all points with a line
                name='Mean Rating',
                line=dict(color='blue'),  # Original color
                marker=dict(color='blue', size=8)
            ))

            # Add a trace for the forecasted points with a different color
            fig.add_trace(go.Scatter(
                x=listings_aggregated['date'][forecast_start_index:],
                y=listings_aggregated['mean_rating'][forecast_start_index:],
                mode='markers+lines',
                name='Forecasted Rating',
                line=dict(color='red'),  # Forecasted color
                marker=dict(color='red', size=8)
            ))

            fig.update_layout(
                title=f'Rating Over Time in {selected_neighborhood}',
                xaxis_title='Date',
                yaxis_title='Rating',
                xaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    tickmode='array',
                    tickvals=listings_aggregated['date'],
                    ticktext=[date.strftime('%Y-%m') for date in listings_aggregated['date']],
                    gridcolor='rgba(0,0,0,0.3)',
                    gridwidth=1,
                ),
                yaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.3)',
                    gridwidth=1,
                ),
                template='plotly',
                margin=dict(l=40, r=40, t=40, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_showspikes=False,
                yaxis_showspikes=False,
                xaxis_showline=True,
                yaxis_showline=True,
                xaxis_linecolor='black',
                yaxis_linecolor='black',
                xaxis_linewidth=2,
                yaxis_linewidth=2,
            )

            return fig, "Rating Over Time"

        else:
            listings_aggregated = listings_filtered.groupby('date').agg(
                mean_price=('price', 'mean')
            ).reset_index()

            # Identify the last two months
            forecast_start_index = -2  # Start of forecasted months

            fig = go.Figure()

            # Add trace for all data points including the connection to the forecasted months
            fig.add_trace(go.Scatter(
                x=listings_aggregated['date'],
                y=listings_aggregated['mean_price'],
                mode='lines',  # Connect all points with a line
                name='Mean Price',
                line=dict(color='green'),  # Original color
                marker=dict(color='green', size=8)
            ))

            # Add a trace for the forecasted points with a different color
            fig.add_trace(go.Scatter(
                x=listings_aggregated['date'][forecast_start_index:],
                y=listings_aggregated['mean_price'][forecast_start_index:],
                mode='markers+lines',
                name='Forecasted Price',
                line=dict(color='orange'),  # Forecasted color
                marker=dict(color='orange', size=8)
            ))

            fig.update_layout(
                title=f'Price Over Time in {selected_neighborhood}',
                xaxis_title='Date',
                yaxis_title='Price',
                xaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    tickmode='array',
                    tickvals=listings_aggregated['date'],
                    ticktext=[date.strftime('%Y-%m') for date in listings_aggregated['date']],
                    gridcolor='rgba(0,0,0,0.3)',
                    gridwidth=1,
                ),
                yaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.3)',
                    gridwidth=1,
                ),
                template='plotly',
                margin=dict(l=40, r=40, t=40, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_showspikes=False,
                yaxis_showspikes=False,
                xaxis_showline=True,
                yaxis_showline=True,
                xaxis_linecolor='black',
                yaxis_linecolor='black',
                xaxis_linewidth=2,
                yaxis_linewidth=2,
            )

            return fig, "Price Over Time"

    @app.callback(
        Output('Amenities', 'figure'),
        [Input('city-dropdown', 'value'),
         Input('neighborhood-dropdown', 'value')]
    )
    def top_10_amenities_graph(selected_city, selected_neighborhood):
        # Check if selected_city or selected_neighborhood is None
        if not selected_city or not selected_neighborhood:
            return go.Figure()  # Return an empty figure if no city or neighborhood is selected
        
        # Filter data for the selected neighborhood and city
        listings_filtered = listings_data.get(selected_city, pd.DataFrame()).loc[
            listings_data[selected_city]['neighbourhood_cleansed'] == selected_neighborhood
        ]
        
        if listings_filtered.empty:
            return go.Figure()  # Return an empty figure if no data
        
        # Select the first row
        first_neighbourhood = listings_filtered.iloc[0]

        # Parse amenities
        parsed_amenities = parse_top_amenities(first_neighbourhood['top_amenities_with_percentages'])

        if not parsed_amenities:
            return go.Figure()  # Return an empty figure if parsing fails
        
        # Prepare data for the bar chart
        amenities_names = [item[0] for item in parsed_amenities]
        amenities_percentages = [item[2] for item in parsed_amenities]

        # Create the bar chart using Plotly
        fig = go.Figure(data=[go.Bar(x=amenities_names, y=amenities_percentages, marker_color='skyblue')])
        fig.update_layout(
            xaxis_title='Top 10 Amenities',
            yaxis_title='Presence in Listings(%)',
            xaxis_tickangle=-45
        )
        return fig

    @app.callback(
        Output('neighborhood-dropdown', 'options'),
        [Input('city-dropdown', 'value')]
    )
    def update_neighborhood_options(selected_city):
        return get_neighborhood_options(listings_data, selected_city)