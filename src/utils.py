import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import config

def get_city_options(city_paths):
    return [{'label': city, 'value': city} for city in city_paths.keys()]

def get_unique_dates(city_paths):
    unique_dates = []
    for city, paths in city_paths.items():
        listings = pd.read_csv(paths['listings'], encoding='utf-8', parse_dates=['date'])
        unique_dates.extend(listings['date'].unique())
    unique_dates = pd.to_datetime(unique_dates).drop_duplicates().sort_values()
    return unique_dates

def update_map(selected_city, selected_month, is_forecasted, city_paths, neighborhoods_geojson, neighborhood_stats):
    if selected_city not in city_paths:
        return html.Div("Invalid city selected")
    
    neighborhoods_geojson_selected = neighborhoods_geojson[selected_city]
    neighborhood_stats_selected = neighborhood_stats[selected_city]
    
    # Filter by the selected month
    neighborhood_stats_filtered = neighborhood_stats_selected[neighborhood_stats_selected['month'] == selected_month]
   
    # Determine the year based on the selected month
    # Assuming that you have a date column or month can be translated into a specific year
    year = 2024  # Adjust this as needed

    if selected_city == 'Madrid, Spain':
        center = {"lat": 40.472775, "lon": -3.703790}
        zoom_level = 9.80
    elif selected_city == 'Barcelona, Spain':
        center = {"lat": 41.389785, "lon": 2.166775}
        zoom_level = 10.9
    elif selected_city == 'Mallorca, Spain':
        center = {"lat": 39.695262, "lon": 3.017571}
        zoom_level = 8.85
    elif selected_city == 'Florence, Italy':
        center = {"lat": 43.769562, "lon": 11.255814}
        zoom_level = 11.0
    elif selected_city == 'Milan, Italy':
        center = {"lat": 45.464204, "lon": 9.189982}
        zoom_level = 10.8
    elif selected_city == 'Rome, Italy':
        center = {"lat": 41.902782, "lon": 12.496366}
        zoom_level = 9.6
    elif selected_city == 'Lisbon, Portugal':
        center = {"lat": 38.936946, "lon": -9.242685}
        zoom_level = 9.0
    elif selected_city == 'Porto, Portugal':
        center = {"lat": 41.157944, "lon": -8.629105}
        zoom_level = 8.9
    else:
        return html.Div("Invalid city selected")

    # Conditional hover data depending on the date
    hover_data = {
        'neighbourhood_cleansed': True,
        'avg_price': ':.2f'
    }
    if not is_forecasted:
        hover_data.update({
            'avg_ratings': ':.2f',
            'name': True
        })

    fig = px.choropleth_mapbox(
        neighborhood_stats_filtered,
        geojson=neighborhoods_geojson_selected,
        locations='neighbourhood_cleansed',
        featureidkey="properties.neighbourhood",
        color="avg_price",
        mapbox_style="carto-positron",
        zoom=zoom_level,
        center=center,
        opacity=0.6,
        title=" ",
        hover_data=hover_data,  # Updated hover data based on the condition
        labels={
            'avg_price': 'Average Price',
            'neighbourhood_cleansed': 'Neighborhood',
            'avg_ratings': 'Average Ratings',
            'name': 'Number of Listings',
        }
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="#F5F5F5",
            font_size=12,
            font_family="Arial",
            font_color="#7F7F7F"
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Average Price",
            tickvals=[neighborhood_stats_filtered['avg_price'].min(), neighborhood_stats_filtered['avg_price'].max()],
            ticktext=["Low", "High"],
            tickcolor="#7F7F7F",
            tickfont=dict(
                color="#7F7F7F"
            ),
            title_font=dict(
                color="#7F7F7F"
            ),
            lenmode="fraction",
            len=1,
            thicknessmode="pixels",
            thickness=20,
            bgcolor="#FFFFFF",
            outlinecolor="#7F7F7F",
            outlinewidth=1
        )
    )

    return dcc.Graph(
        id='map',
        figure=fig,
        style={'width': '100%', 'height': '750px', 'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}
    )

def generate_table(dataframe, width=1000, height=600):
    headerColor = config.COLORS['primary']
    rowEvenColor = config.COLORS['light']
    rowOddColor = config.COLORS['background']

    dataframe.columns = ['Price' if col == 'price' else 
                         'Rating' if col == 'review_scores_rating' else 
                         'Name' if col == 'name' else
                         'Room Type' if col == 'room_type' else
                         'Reviews' if col == 'number_of_reviews' else
                         'Min. Nights' if col == 'minimum_nights' else
                         'Host' if col == 'host_name' else
                         'ID' if col == 'id' else
                         'Category(NLP)' if col == 'category' else
                         'Positivity_Score(1to5)(NLP)' if col == 'Positivity_Score(1to5)' else
                         col for col in dataframe.columns]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f'<b>{col}</b>' for col in dataframe.columns],
            line_color=headerColor,  # Set line color same as header color for solid appearance
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[dataframe[col] for col in dataframe.columns],
            line_color=rowOddColor,  # Set line color for cells
            fill_color=[[rowOddColor, rowEvenColor]*len(dataframe)],
            align=['left', 'center'],
            font=dict(color=config.COLORS['text'], size=12),
            height=30,  # Adjust height for spacing
        )
    )])

    fig.update_layout(
        width=width, 
        height=height,
        #margin=dict(l=10, r=10, t=10, b=10),  # Adjust margins if needed
        paper_bgcolor='white',  # Ensure paper background is white
        plot_bgcolor='white'    # Ensure plot background is white
    )

    return dcc.Graph(figure=fig)    
    
####return dcc.Graph(figure=fig)

def get_sort_options(listings_data, selected_city):
    if selected_city in listings_data:
        columns = config.DEFAULT_COLUMNS + config.ADDITIONAL_COLUMNS_LIST
        available_columns = [col for col in columns if col in listings_data[selected_city].columns]
        return [{'label': config.COLUMN_DISPLAY_NAMES.get(col, col), 'value': col} for col in available_columns]
    return []

def get_column_options(listings_data, selected_city):
    if selected_city in listings_data:
        all_columns = listings_data[selected_city].columns
        additional_columns = [col for col in config.ADDITIONAL_COLUMNS_LIST if col in all_columns]
        return [{'label': config.COLUMN_DISPLAY_NAMES.get(col, col), 'value': col} for col in additional_columns]
    return []

def get_neighborhood_options(listings_data, selected_city):
    if selected_city in listings_data:
        neighborhoods = listings_data[selected_city]['neighbourhood_cleansed'].unique()
        return [{'label': neighborhood, 'value': neighborhood} for neighborhood in neighborhoods]
    return []

def parse_top_amenities(amenities_str):
    amenities = amenities_str.split("), ")  # Split by "), " to handle both parts together
    parsed_data = []
    
    for amenity in amenities:
        try:
            # Further splitting to remove brackets
            name, count_percentage = amenity.split(" (")
            count, percentage = count_percentage.split(", ")
            count = int(count)
            percentage = float(percentage.strip('%)'))
            parsed_data.append((name, count, percentage))
        except ValueError as e:
            print(f"Skipping malformed amenity: {amenity} due to error: {e}")
    
    return parsed_data