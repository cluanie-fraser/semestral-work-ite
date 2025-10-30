  
import unittest
# Import the function we want to test from the main script
from main import fetch_movie_details, API_KEY

# Since these tests hit the live TMDB API, they are known as "Integration Tests".

class TestMovieFetcher(unittest.TestCase):
    """
    Test suite for the fetch_movie_details function.
    """


    def test_known_movie_success(self):
        """Test fetching a well-known movie (Inception) to ensure data is returned."""
        # Arrange
        movie_title = "Inception"
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        self.assertIsNotNone(details, "Details should not be None (API call failed)")
        self.assertIsInstance(details, dict, "Result should be a dictionary")
        self.assertEqual(details['title'], "Inception", "Title should match the expected movie")
        self.assertIn('/10', details['rating'], "Rating should be present and formatted with /10")

    def test_known_movie_with_partial_match(self):
        """Test fetching a partial movie title (The Matrix) to ensure it finds the correct movie."""
        # Arrange
        movie_title = "Matrix" 
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        self.assertIsNotNone(details, "Details should not be None")
        # TMDB's search is good; it should still return the full, correct title as the first result.
        self.assertIn("Matrix", details['title'], "Title should contain 'Matrix'")
        self.assertGreater(len(details['cast']), 10, "Cast list should be longer than 10 characters")

    def test_non_existent_movie_failure(self):
        """Test searching for a movie that should not exist to ensure it returns None."""
        # Arrange
        movie_title = "ThisMovieDefinitelyDoesNotExist987654321"
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        self.assertIsNone(details, "Details should be None for a non-existent movie")
        
    def test_empty_string_search(self):
        """Test searching with an empty string to ensure appropriate handling (TMDB might return popular movies)."""
        # Arrange
        movie_title = ""
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        # An empty query often returns the most popular movie, so we assert that *something* is returned.
        self.assertIsNotNone(details, "Details should not be None for an empty search")
        self.assertIsInstance(details, dict, "Result should be a dictionary")


# This is the standard way to run unittest from a file
if __name__ == "__main__":
    unittest.main()

