# semestral-work-ite
#  Movie Details Fetcher

A simple Python command-line script that fetches and displays key details about a movie using The Movie Database (TMDB) API from user requested titles.

## ✨ How to use & Features

* **Search by Title:** Find a movie by entering its name.
* **Detailed Information:** Displays the TMDB rating, release date, and runtime.
* **Main Cast:** Shows the top 5 credited cast members.
* **Retry:** If the movie is incorrect, the program provides an option to display search results of other movies with similar titles. 

---

## 🚀 Setup and Installation

### Prerequisites

You need **Python 3** installed on your system and an **API Key** from TMDB.

1.  **Get an API Key:** Sign up for an account at [The Movie Database (TMDB)](https://www.themoviedb.org/) and generate a personal API key.

2.  **Install Dependencies:** This project requires the `requests` python library to handle API calls. This can be installed on your respective python IDE


### Configuration

Open the `main.py` file and replace the placeholder value with your actual TMDB API key:

```python
# main.py (Excerpt)
API_KEY = "YOUR_API_KEY_HERE"  # <-- Update this line
BASE_URL = "[https://api.themoviedb.org/3](https://api.themoviedb.org/3)"
```

### Test.md
The file `test.md` describes the testing approach and mindset


### Known Issues
