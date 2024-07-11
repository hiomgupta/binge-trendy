from flask import Flask, render_template, request
import re
import requests
import pandas as pd
import numpy as np
from sklearn import linear_model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        season = request.form.get('season')
        api_key = "45e41d0c"  # Hardcoded API key

        # Extract IMDb ID from the URL
        imdbID = [x for x in url.split("/") if re.match('tt', x)][0]

        # OMDb API URL for the TV show
        omdb_url = "http://www.omdbapi.com/?i=" + imdbID + "&apikey=" + api_key
        omdb_url_req = requests.get(omdb_url)

        # Check for a valid response from the OMDb API
        if omdb_url_req.status_code != 200:
            return f"Error: {omdb_url_req.status_code}"

        # Get the title of the series
        series_title = omdb_url_req.json()['Title']
        total_seasons = omdb_url_req.json()['totalSeasons']

        # Determine the season(s) of interest
        season = [season] if season else list(range(1, int(total_seasons) + 1))

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

        # Output the requested results
        highest_residual = df_residuals[df_residuals['Residual'] == df_residuals['Residual'].max()].to_string(index=False)
        top_ten = df_residuals.sort_values(by=['Residual'], ascending=False)[:10].to_string(index=False)
        season_info = df_residuals[['Season', 'Episode', 'Name', 'Residual']].to_string(index=False)

        return render_template('index.html', series_title=series_title, season_info=season_info, highest_residual=highest_residual, top_ten=top_ten)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
