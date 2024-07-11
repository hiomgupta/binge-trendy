import argparse
import re
import requests
import sys
import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Command line utility to determine which TV show episodes are above the norm for a season as rated by IMDb users for more informed binge watching")

# Add arguments
parser.add_argument('-url', help="IMDb show URL of interest", required=True)
parser.add_argument('-key', help="Text file with OMDb API key", type=argparse.FileType("r"), required=False)
parser.add_argument('-s', help="Season of interest")
parser.add_argument('-b', help="Episode with the highest residual", action='store_true')
parser.add_argument('-tt', help="List of top ten rated episodes of show", action='store_true')

# Parse arguments
args = parser.parse_args()

# Extract IMDb ID from the URL
imdbID = [x for x in args.url.split("/") if re.match('tt', x)][0]

# Read the OMDb API key
api_key = "45e41d0c"

# OMDb API URL for the TV show
omdb_url = "http://www.omdbapi.com/?i=" + imdbID + "&apikey=" + api_key
omdb_url_req = requests.get(omdb_url)

# Check for a valid response from the OMDb API
if omdb_url_req.status_code != 200:
    print("Error: https://http.cat/" + str(omdb_url_req.status_code))
    sys.exit(1)

# Get the title of the series
series_title = omdb_url_req.json()['Title']

# Get the total number of seasons
total_seasons = omdb_url_req.json()['totalSeasons']

# Determine the season(s) of interest
season = [args.s] if args.s else list(range(1, int(total_seasons) + 1))

# Initialize a DataFrame to store the results
summary_list = ["Season", "Episode", "Value", "Name"]
final_df = pd.DataFrame()

# Process each season
for x in season:
    omdb_season_url = "http://www.omdbapi.com/?i=" + imdbID + "&Season=" + str(x) + "&apikey=" + api_key
    omdb_season_url_req = requests.get(omdb_season_url)

    episode = [float(y['Episode']) for y in omdb_season_url_req.json()['Episodes']]
    rating = [y['imdbRating'] for y in omdb_season_url_req.json()['Episodes']]
    title = [y['Title'] for y in omdb_season_url_req.json()['Episodes']]
    local_season = [x] * len(omdb_season_url_req.json()['Episodes'])
    df = pd.DataFrame([local_season, episode, rating, title]).transpose()
    df.columns = summary_list

    df = df[df.Value != 'N/A']
    df['Value'] = df['Value'].astype(float)
    df_sorted = df.sort_values(by='Episode')

    x_values = np.array(df_sorted['Episode']).reshape(-1, 1)
    y_values = np.array(df_sorted['Value']).reshape(-1, 1)
    if len(df_sorted) > 1:
        reg = linear_model.LinearRegression()
        reg.fit(x_values, y_values)
        df_sorted['Prediction'] = reg.predict(x_values).flatten()  # Ensure this is a 1D array
        df_sorted['Residual'] = df_sorted['Value'] - df_sorted['Prediction']  # Ensure subtraction is between 1D arrays
        final_df = pd.concat([final_df, df_sorted])

# Filter out rows with positive residuals
df_residuals = final_df.query('Residual > 0.0')
df_residuals = df_residuals.drop(columns=['Value'])

# Plot IMDb Ratings vs. Episode Numbers with Linear Regression Line
if not final_df.empty:
    season_info = f"{series_title} - Season {args.s}" if args.s else series_title
    fig, ax = plt.subplots()
    ax.scatter(final_df['Episode'], final_df['Value'], label='IMDb Ratings', color='blue')
    ax.plot(final_df['Episode'], final_df['Prediction'], label='Linear Regression', color='red')
    ax.set_xlabel('Episode Number')
    ax.set_ylabel('IMDb Rating')
    ax.set_title(f'{season_info}')
    ax.legend()
    plt.show()


# Output the requested results
if args.b:
    print(df_residuals[df_residuals['Residual'] == df_residuals['Residual'].max()].to_string(index=False))
if args.tt:
    print(df_residuals.sort_values(by=['Residual'], ascending=False)[:10].to_string(index=False))
if args.s:
    print(df_residuals[['Season', 'Episode', 'Name', 'Residual']].to_string(index=False))
