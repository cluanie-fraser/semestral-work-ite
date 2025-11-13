import unittest
# Import the new functions we want to test
from main import fetch_search_results, fetch_details_by_index

# Since these tests hit the live TMDB API, they are known as "Integration Tests".

class TestMovieFetcher(unittest.TestCase):
    """
    Test suite for the movie fetcher functions.
    """

    def test_known_movie_success_flow(self):
        """
        Test the full, successful flow:
        1. Search for a known movie ("Inception").
        2. Fetch the details for the first result (index 0).
        3. Verify the specific data is correct.
        """
        # Arrange
        movie_title = "Inception"
        
        # Expected Values for Inception
        EXPECTED_RATING = "8.4/10"
        EXPECTED_RUNTIME = "148 minutes"
        EXPECTED_RELEASE_DATE = "2010-07-15"
        EXPECTED_CAST = "Leonardo DiCaprio, Joseph Gordon-Levitt, Ken Watanabe, Tom Hardy, Elliot Page"

        # Act (Step 1: Search)
        search_data = fetch_search_results(movie_title)
        
        # Assert (Step 1)
        self.assertIsNotNone(search_data, "Search results should not be None")
        self.assertGreater(len(search_data.get('results', [])), 0, "Search 'results' list should not be empty")

        # Act (Step 2: Fetch Details for first result)
        details = fetch_details_by_index(search_data, 0)

        # Assert (Step 2)
        self.assertIsNotNone(details, "Details should not be None (API call failed)")
        self.assertIsInstance(details, dict, "Result should be a dictionary")
        self.assertEqual(details['title'], "Inception", "Title should match the expected movie")
        
        # New, specific assertions for the movie's data
        self.assertEqual(details['rating'], EXPECTED_RATING)
        self.assertEqual(details['runtime'], EXPECTED_RUNTIME)
        self.assertEqual(details['release_date'], EXPECTED_RELEASE_DATE)
        self.assertEqual(details['main_cast'], EXPECTED_CAST)

    def test_search_partial_match(self):
        """Test the search function for a partial title ("Interstell")."""
        # Arrange
        movie_title = "Interstell" 
        
        # Act
        search_data = fetch_search_results(movie_title)
        details = fetch_details_by_index(search_data, 0)
        
        # Assert
        self.assertIsNotNone(details, "Details should not be None")
        self.assertIn("Interstell", details['title'], "Title should contain 'Interstell'")
        self.assertGreater(len(details['main_cast']), 10, "Cast list should be longer than 10 characters")

    def test_search_non_existent_movie(self):
        """Test the SEARCH function for a movie that should not exist."""
        # Arrange
        movie_title = "ThisMovieDefinitelyDoesNotExist987654321"
        
        # Act
        search_data = fetch_search_results(movie_title)
        
        # Assert
        self.assertIsNone(search_data, "Search results should be None for a non-existent movie")
        
    def test_search_empty_string(self):
        """Test the SEARCH function with an empty string."""
        # Arrange
        movie_title = ""
        
        # Act
        search_data = fetch_search_results(movie_title)
        
        # Assert
        self.assertIsNone(search_data, "Search results should be None for an empty string")

    def test_fetch_details_with_bad_index(self):
        """
        Test the FETCH DETAILS function to ensure it fails gracefully
        if given an index that is out of bounds.
        """
        # Arrange: First, get valid search data
        movie_title = "Inception"
        search_data = fetch_search_results(movie_title)
        self.assertIsNotNone(search_data, "Setup for bad index test failed: Search returned None")

        # Act: Try to fetch an index that doesn't exist (e.g., 99)
        bad_index = 99
        details = fetch_details_by_index(search_data, bad_index)
        
        # Assert
        self.assertIsNone(details, "Details should be None when a bad index is provided")


# This is the standard way to run unittest from a file
if __name__ == "__main__":
    unittest.main()