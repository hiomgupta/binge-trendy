# Binge Trendy

A Python program to help you binge-watch smarter by listing only the best TV show episodes.
GraphTV plots the IMDb user ratings for every episode and then performs a linear regression of the episode rating on the episode number to make a trend line. I have personally found that watching only the shows above the trend line means I watch the good episodes and skip the bad ones (i.e. the ones below the trend line). I also wanted a good reason to use OMDb API.

Of course, this will only work for TV shows where you can watch a few episodes here and there and not for shows like The Greatest Show Ever.

I have personally developed the Python part of this project. I received help from Chat GPT for web development and other aspects.

## Tech Used

- **Python**: The core logic and data processing.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations.
- **sci-kit-learn**: Machine learning library for linear regression.

## Why Linear Regression?

Linear regression is used in this project to establish a trend line for episode ratings across seasons. We can identify episodes that stand out by comparing each episode's rating to the predicted value on this trend line. Based on the overall trend, these episodes are likely to be more enjoyable as they perform better than expected.

![ALt text](/images/Figure_1.png)

## How It Works

1. **Input**: Users provide the IMDb URL of a TV show and optionally specify a season.
2. **Processing**: The app fetches episode ratings from the OMDb API, performs linear regression to determine the trend, and calculates each episode's rating deviation from the predicted trend.
3. **Output**: Episodes with positive deviations (better than expected) are highlighted as the best episodes.

## Example

Here's an example using "Game of Thrones" (Season 1):

| Season | Episode | Name              | Deviation |
|--------|---------|-------------------|-----------|
| 1      | 9       | Baelor            | 1.2       |
| 1      | 10      | Fire and Blood    | 0.8       |
| 1      | 6       | A Golden Crown    | 0.7       |

### Graph Example

![IMDb Ratings vs. Episode Numbers with Linear Regression Line](static/example_graph.png)

## Website

The application is also deployed and can be accessed at [URL](http://bingetrendy.com).
