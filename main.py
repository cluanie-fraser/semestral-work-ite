import requests

# --- Configuration ---
# TMDB API documentation: https://www.themoviedb.org/documentation/api
API_KEY = "77dbe92dcb0fe1ff2c8aa82f7b391e19" 
BASE_URL = "https://api.themoviedb.org/3"

def fetch_search_results(title):
    """
    Performs the initial search query and returns the raw JSON data.

    :param title: The title of the movie to search for (string).
    :return: The full search results dictionary or None on error.
    """
    print(f"\n--- Searching for: {title} ---")
    search_url = f"{BASE_URL}/search/movie"
    search_params = {
        "api_key": API_KEY,
        "query": title
    }
    
    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get('results'):
            print("Error: No movie found with that title.")
            return None
        
        return search_data
    
    # if new user forgets to include their own API key:
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

def fetch_details_by_index(search_data, index):
    """
    Fetches detailed info and cast for a movie based on its index in the search results.

    :param search_data: The full search results dictionary.
    :param index: The index (0 for first, 1 for second, etc.) of the movie to fetch.
    :return: A formatted results dictionary or None on error.
    """
    try:
        # Check if the requested index exists in the results list
        if index >= len(search_data['results']):
            print(f"Error: No movie found at index {index} in the search results.")
            return None

        # Extract the necessary data for the selected movie
        selected_movie = search_data['results'][index]
        movie_id = selected_movie['id']
        found_title = selected_movie['title']
        print(f"Found movie ID: {movie_id} (Result #{index + 1}: {found_title})")

        # 1. FETCH DETAILED MOVIE INFORMATION (Rating, Runtime, Release Date)
        details_url = f"{BASE_URL}/movie/{movie_id}"
        details_params = {
            "api_key": API_KEY,
        }
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details = details_response.json()

        # 2. FETCH CAST INFORMATION (Credits)
        credits_url = f"{BASE_URL}/movie/{movie_id}/credits"
        credits_response = requests.get(credits_url, params=details_params)
        credits_response.raise_for_status()
        credits = credits_response.json()

        # 3. EXTRACT AND FORMAT DATA
        cast_list = [member['name'] for member in credits.get('cast', [])[:5]]
        cast_display = ", ".join(cast_list) if cast_list else "N/A"

        rating = details.get('vote_average', 'N/A')
        release_date = details.get('release_date', 'N/A')
        runtime = details.get('runtime', 'N/A') 
        
        formatted_rating = f"{rating:.1f}/10" if isinstance(rating, float) else rating
        formatted_runtime = f"{runtime} minutes" if runtime != 'N/A' else 'N/A'
        
        results = {
            'title': found_title,
            'rating': formatted_rating,
            'release_date': release_date,
            'runtime': formatted_runtime,
            'main_cast': cast_display,
            # Used by unit tests but not displayed to user:
            'raw_runtime': runtime, 
            'raw_rating': rating
            }

        return results

    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occurred while fetching details: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the details request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def display_results(data):
    """Prints the formatted movie details to the console."""
    if data:
        print("\n========================================")
        print(f"Movie Title: {data['title']}")
        print("========================================")
        print(f"Rating (TMDB): {data['rating']}")
        print(f"Release Date:  {data['release_date']}")
        print(f"Runtime:       {data['runtime']}")
        print(f"Main Cast:     {data['main_cast']}")
        print("========================================\n")
        return True
    return False


# --- Main entry point for command-line execution ---
if __name__ == "__main__":
    # 1. Prompt the user for a movie title
    user_input = input("Enter a movie title: ")
    
    # 2. Perform the initial search
    search_results = fetch_search_results(user_input)
    
    if search_results:
        current_index = 0
        
        # Loop to allow user to retry if the first movie is incorrect
        while current_index < len(search_results['results']):
            
            # Fetch and format details for the movie at the current index
            movie_details = fetch_details_by_index(search_results, current_index)
            
            # Display the results
            if display_results(movie_details):
                # Now ask the user if they want to retry
                prompt = input(f"Is '{movie_details['title']}' correct? Type 'retry' for the next suggestion or press Enter to exit: ").strip().lower()
                
                if prompt == "retry":
                    # Move to the next movie result
                    current_index += 1
                    # Check if we ran out of results
                    if current_index >= len(search_results['results']):
                        print("No more search results available.")
                        break # Exit the loop
                else:
                    # User accepted the movie or pressed Enter to quit
                    break # Exit the loop
            else:
                # If fetching details failed for the current index, exit the loop
                break
            
    else:
        print(f"\n--- Searching for: {user_input} ---")
        print("Operation failed or no search results were retrieved.")