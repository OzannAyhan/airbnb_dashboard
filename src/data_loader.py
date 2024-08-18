import json
import pandas as pd
import config

def load_data(city_paths):
    neighborhoods_geojson = {}
    neighborhood_stats = {}
    listings_data = {}

    for city, paths in city_paths.items():
        try:
            with open(paths['geojson'], 'r') as file:
                neighborhoods_geojson[city] = json.load(file)
        except FileNotFoundError:
            print(f"GeoJSON file for {city} not found at {paths['geojson']}")
            continue

        try:
            with open(paths['listings'], 'r', encoding='utf-8', errors='replace') as file:
                listings = pd.read_csv(file, parse_dates=['date']).dropna(subset=['neighbourhood_cleansed', 'price'])
        except FileNotFoundError:
            print(f"Listings CSV file for {city} not found at {paths['listings']}")
            continue

        listings['month'] = listings['date'].dt.month

        agg_columns = {
            'price': 'mean',
            'review_scores_rating': 'mean',
            'number_of_reviews': 'mean',
            'name': 'count'
        }

        available_columns = [col for col in agg_columns.keys() if col in listings.columns]
        if not available_columns:
            print(f"No columns to aggregate in listings for {city}")
            continue

        neighborhood_stats[city] = listings.groupby(['neighbourhood_cleansed', 'month'])[available_columns].agg(agg_columns).reset_index()
        if 'price' in neighborhood_stats[city].columns:
            neighborhood_stats[city] = neighborhood_stats[city].rename(columns={'price': 'avg_price'})
        if 'review_scores_rating' in neighborhood_stats[city].columns:
            neighborhood_stats[city] = neighborhood_stats[city].rename(columns={'review_scores_rating': 'avg_ratings'})

        listings_data[city] = listings[['date', 'month', 'price', 'neighbourhood_cleansed', 'review_scores_rating', 'name', 'host_total_listings_count', 
                                'number_of_reviews', 'id',  'host_name', 'host_id', 'reviews_per_month','top_amenities_with_percentages','Positivity_Score(1to5)','category'
                                ]].copy()

    return neighborhoods_geojson, neighborhood_stats, listings_data

neighborhoods_geojson, neighborhood_stats, listings_data = load_data(config.CITY_PATHS)