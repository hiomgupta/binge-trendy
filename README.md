# Binge Trendy

A Python program to help you binge watch smarter by only listing the best episodes of TV shows. (UPDATE: now live at [URL](https://hiomgupta.github.io/binge-trendy/))

GraphTV plots the IMDb user ratings for every episode and then performs a linear regression of the episode rating on the episode number to make a trend line. I have personally found that watching only the shows above the trend line means I just watch the good episodes and skip the bad ones (i.e. the ones below the trend line). I also wanted a good reason to use OMDb API.

Of course, this will only work for TV shows where you can just watch a few episodes here and there and not for shows like the greatest show ever.

I have personally developed the Python part of this project. For the web development and other aspects, I received help from Chat GPT.

## Tech Used

- **Python**: The core logic and data processing.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations.
- **scikit-learn**: Machine learning library for linear regression.

## Why Linear Regression?

Linear regression is used in this project to establish a trend line for episode ratings across a season. By comparing each episode's rating to the predicted value on this trend line, we can identify episodes that stand out. These episodes are likely to be more enjoyable as they perform better than expected based on the overall trend.

! [ALt text](/images/Figure_1.png)

## How It Works

1. **Input**: Users provide the IMDb URL of a TV show and optionally specify a season.
2. **Processing**: The app fetches episode ratings from the OMDb API, performs linear regression to determine the trend, and calculates the deviation of each episode's rating from the predicted trend.
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
