  
import unittest
# Import the function we want to test from the main script
from main import fetch_movie_details

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
        self.assertRegex(details['release_date'], r'\d{4}-\d{2}-\d{2}', "Release date should be present and formatted as YYYY-MM-DD")
        self.assertTrue('runtime' in details and len(str(details['runtime'])) > 0, "Runtime should be present and non-empty")
        
    def test_known_movie_with_partial_match(self):
        """Test fetching a partial movie title (Interstellar) to ensure it finds the correct movie."""
        # Arrange
        movie_title = "Interstell" 
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        self.assertIsNotNone(details, "Details should not be None")
        # TMDB's search is good; it should still return the full, correct title as the first result.
        self.assertIn("Interstell", details['title'], "Title should contain 'Interstell'")
        self.assertGreater(len(details['main_cast']), 10, "Cast list should be longer than 10 characters")

    def test_non_existent_movie_failure(self):
        """Test searching for a movie that should not exist to ensure it returns None."""
        # Arrange
        movie_title = "ThisMovieDefinitelyDoesNotExist987654321"
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        self.assertIsNone(details, "Details should be None for a non-existent movie")
        
    def test_empty_string_search_failure(self):
        """Test searching with an empty string to ensure it correctly returns None."""
        # Arrange
        movie_title = ""
        
        # Act
        details = fetch_movie_details(movie_title)
        
        # Assert
        # TMDB's /search/movie for query='' often returns no results, leading to an intentional failure.
        self.assertIsNone(details, "Details should be None for an empty search, as no specific title is provided.")


# This is the standard way to run unittest from a file
if __name__ == "__main__":
    unittest.main()

