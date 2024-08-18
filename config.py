import os

# Define the path to the local data directory
DATASET_DIR = 'data/'

DEBUG = True

CITY_PATHS = {
    'Madrid, Spain': {
        'listings': os.path.join(DATASET_DIR, 'madrid_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_madrid.geojson')
    },
    'Barcelona, Spain': {
        'listings': os.path.join(DATASET_DIR, 'barcelona_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_barcelona.geojson')
    },
    'Mallorca, Spain': {
        'listings': os.path.join(DATASET_DIR, 'mallorca_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_mallorca.geojson')
    },
    'Florence, Italy': {
        'listings': os.path.join(DATASET_DIR, 'florence_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_florence.geojson')
    },
    'Milan, Italy': {
        'listings': os.path.join(DATASET_DIR, 'milan_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_milan.geojson')
    },
    'Rome, Italy': {
        'listings': os.path.join(DATASET_DIR, 'rome_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_rome.geojson')
    },
    'Lisbon, Portugal': {
        'listings': os.path.join(DATASET_DIR, 'lisbon_final_data.csv'),
        'geojson': os.path.join(DATASET_DIR, 'neighbourhoods_lisbon.geojson')
    }
}

COLORS = {
    'background': '#F5F5F5',
    'text': '#333333',
    'primary': '#FF5A5F',
    'secondary': '#767676',
    'accent': '#00A699',
    'info': '#FC642D',
    'light': '#FFFFFF',
    'dark': '#484848'
}

COLUMN_DISPLAY_NAMES = {
    'neighbourhood_cleansed': 'Neighbourhood',
    'name': 'Name',
    'host_id': 'Host ID',
    'host_name': 'Host',
    'room_type': 'Room Type',
    'number_of_reviews': 'Reviews',
    'reviews_per_month': 'Reviews/Month',
    'id': 'ID',
    'minimum_nights': 'Min. Nights',
    'price': 'Price',
    'review_scores_rating': 'Rating',
    'month': 'Month',
    'Positivity_Score(1to5)': 'Positivity_Score(1to5)(NLP)',
    'category': 'Category(NLP)'
}

ADDITIONAL_COLUMNS_LIST = [
    'host_name',
    'number_of_reviews',
    'category',
    'Positivity_Score(1to5)'
]

DEFAULT_COLUMNS = ['price', 'review_scores_rating', 'name', 'id']