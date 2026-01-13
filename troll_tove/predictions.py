"""
Prediction logic module for Troll-Tove app.

Handles loading predictions from files and selecting predictions
based on various criteria. Separates prediction logic from presentation.
"""
import logging
from typing import List

logger = logging.getLogger(__name__)


def load_predictions_from_file(filename: str) -> List[str]:
    """
    Load predictions from a text file.
    
    Args:
        filename: Path to the prediction file
        
    Returns:
        List of prediction strings, or fallback messages on error
    """
    try:
        with open(filename, "r", encoding="utf-8") as file_handle:
            predictions = [line.strip() for line in file_handle if line.strip()]
        if not predictions:
            logger.warning(f"No predictions found in {filename}")
            return ["Troll-Tove ser ingen ting i dag... Prøv igjen seinere."]
        return predictions
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return ["Troll-Tove har mista spådomsboka si... Kom tilbake seinere!"]
    except Exception as error:
        logger.error(f"Error reading {filename}: {error}")
        return ["Noko gikk gale... Troll-Tove e forvirra!"]


class PredictionSelector:
    """
    Handles prediction selection logic.
    
    Provides methods for deterministic and random selection of predictions
    while keeping the selection logic separate from the prediction content.
    """
    
    def __init__(self, fotball_predictions: List[str], random_predictions: List[str]):
        """
        Initialize with loaded predictions.
        
        Args:
            fotball_predictions: List of football-related predictions
            random_predictions: List of general/dark predictions
        """
        self.fotball_predictions = fotball_predictions
        self.random_predictions = random_predictions
    
    def get_all_predictions(self) -> List[str]:
        """Get combined list of all predictions."""
        return self.fotball_predictions + self.random_predictions
    
    def get_fotball_prediction(self) -> List[str]:
        """Get only football predictions."""
        return self.fotball_predictions
    
    def get_random_prediction(self) -> List[str]:
        """Get only random/dark predictions."""
        return self.random_predictions
    
    def count_predictions(self) -> dict:
        """
        Get count of available predictions.
        
        Returns:
            Dictionary with counts by category
        """
        return {
            "fotball": len(self.fotball_predictions),
            "random": len(self.random_predictions),
            "total": len(self.get_all_predictions())
        }
