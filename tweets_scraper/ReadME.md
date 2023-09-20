# Setting up Conda Environment for Scraper

Follow these steps to set up a Conda environment for your scraper using Python 3.11.

## Prerequisites

- Conda (Miniconda or Anaconda) installed on your system. If not installed, download and install it from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual).

## Setup Instructions

1. Clone or download the project repository to your local machine.

```
git clone https://github.com/yourusername/x_scraper.git
cd x_scraper
```

2. Create a Conda environment using the provided `requirements.txt` file. Replace `myenv` with your desired environment name:

```
conda create --name scraper -c conda-forge python=3.11 --file requirements.txt
```

- `--name scraper`: Replace `scraper` with your preferred environment name.
- `-c conda-forge`: Specifies the Conda channel (you can change this channel if needed).
- `python=3.11`: Specifies the Python version (change as per your requirements).
- `--file requirements.txt`: Installs packages listed in the `requirements.txt` file.

3. Activate the Conda environment:

```
conda activate scraper
```

Now you have successfully set up and activated your Conda environment for the scraper. You can start working on your project within this environment.

To deactivate the environment when you are done, simply run:

```
conda deactivate
```


4. To fetch trending tweets of the day

```
python fetch_trending_tweets_of_the_day.py
```

5. To fetch results for a typed search query

python search_query_tweets.py


6. auth token in the config files must be updated (using inspect tool in browser) if session expires, and always add a sleep time of 1s


### Check if your requirements are bound to terms and conditions

[Twitter Scraping Permissions](https://www.twitter.com/robots.txt).

