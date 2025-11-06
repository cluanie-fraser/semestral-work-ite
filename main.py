

import requests

# --- Configuration ---
# TMDB API documentation: https://www.themoviedb.org/documentation/api
API_KEY = "77dbe92dcb0fe1ff2c8aa82f7b391e19" 
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_details(title):
    """
    Fetches and displays details for a given movie title from TMDB.

    :param title: The title of the movie to search for (string).
    """

    print(f"\n--- Searching for: {title} ---")

    # 1. SEARCH FOR THE MOVIE TITLE to get the movie ID
    search_url = f"{BASE_URL}/search/movie"
    search_params = {
        "api_key": API_KEY,
        "query": title
    }

    try:
        # Perform the search request
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        search_data = search_response.json()

        # Check if any results were found
        if not search_data.get('results'):
            print("Error: No movie found with that title. Try again")
            return

        # Use the first result (most relevant)
        movie_id = search_data['results'][0]['id']
        found_title = search_data['results'][0]['title']
        print(f"Found movie ID: {movie_id} ({found_title})")


        # 2. FETCH DETAILED MOVIE INFORMATION (Rating, Runtime, Release Date)
        details_url = f"{BASE_URL}/movie/{movie_id}"
        details_params = {
            "api_key": API_KEY,
        }
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details = details_response.json()

        # 3. FETCH CAST INFORMATION (Credits)
        credits_url = f"{BASE_URL}/movie/{movie_id}/credits"
        credits_response = requests.get(credits_url, params=details_params) # Reusing details_params
        credits_response.raise_for_status()
        credits = credits_response.json()

        # 4. EXTRACT AND FORMAT DATA
        
        # Get up to the first 5 cast members
        cast_list = [member['name'] for member in credits.get('cast', [])[:5]]
        cast_display = ", ".join(cast_list) if cast_list else "N/A"

        # Extract basic details
        rating = details.get('vote_average', 'N/A')
        release_date = details.get('release_date', 'N/A')
        runtime = details.get('runtime', 'N/A') # Runtime is in minutes
        
        # Convert rating to a nice format (out of 10)
        formatted_rating = f"{rating:.1f}/10" if isinstance(rating, float) else rating
        
        # Format runtime for readability
        formatted_runtime = f"{runtime} minutes" if runtime != 'N/A' else 'N/A'
        
        # Results dictionary for unit test
        results = {
            'title': found_title,
            'rating': formatted_rating,
            'release_date': release_date,
            'runtime': formatted_runtime,
            'main_cast': cast_display,
            'raw_runtime': runtime, # Add raw runtime for easier assertion
            'raw_rating': rating
            
            }

        return results

    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
        print("Tip: Did you include a valid TMDB API key?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Main entry point for command-line execution ---
if __name__ == "__main__":
    # 1. Prompt the user for a movie title
    user_input = input("Enter a movie title: ")
    
    # 2. Call the function with the user's input
    data = fetch_movie_details(user_input)
    
    
    # 3. DISPLAY THE RESULTS - results will only be printed if this
    # file is run directly
    if data:
        print("\n========================================")
        print(f"Movie Title: {data['title']}")
        print("========================================")
        print(f"Rating (TMDB): {data['rating']}")
        print(f"Release Date:  {data['release_date']}")
        print(f"Runtime:       {data['runtime']}")
        print(f"Main Cast:     {data['main_cast']}")
        print("========================================\n")
        
    elif user_input:
        print(f"\n--- Searching for: {user_input} ---")
        print("Error: Could not retrieve movie details or no movie found.")

