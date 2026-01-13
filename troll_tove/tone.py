"""
Tone and text formatting module for Troll-Tove app.

Handles intro messages, response formatting, and the humorous/dark tone
of the app. Keeps humor and presentation logic separate from prediction logic.
"""


class ToneFormatter:
    """
    Handles tone and text formatting for different modes.
    
    Provides intro messages and formatting specific to different modes
    (standard, Glimt, dark) while keeping the tone separate from logic.
    """
    
    @staticmethod
    def format_standard_intro(user_name: str) -> str:
        """
        Format intro message for standard mode.
        
        Args:
            user_name: User's name or default
            
        Returns:
            Formatted intro message
        """
        return f"Hør hør, {user_name}! Troll-Tove har kikka i kula si…"
    
    @staticmethod
    def format_glimt_intro(user_name: str = "du jævel") -> str:
        """
        Format intro message for Glimt mode.
        
        Args:
            user_name: User's name (defaults to cheeky nickname)
            
        Returns:
            Formatted intro message with Glimt-specific tone
        """
        return f"Hør hør, {user_name.title()}! Troll-Tove har sett lyset fra Aspmyra…"
    
    @staticmethod
    def format_dark_intro(user_name: str = "kompis") -> str:
        """
        Format intro message for dark mode.
        
        Args:
            user_name: User's name (defaults to "kompis")
            
        Returns:
            Formatted intro message with dark/existential tone
        """
        return f"Mørke skyer samler seg, {user_name}… Troll-Tove ser noe dystert i horisonten."
    
    @staticmethod
    def sanitize_user_name(user_name: str, max_length: int = 100) -> str:
        """
        Sanitize and validate user name input.
        
        Args:
            user_name: Raw user name input
            max_length: Maximum allowed length
            
        Returns:
            Sanitized name or default "Du"
        """
        if not user_name or len(user_name) > max_length:
            return "Du"
        return user_name.strip()
    
    @staticmethod
    def sanitize_question(question: str, max_length: int = 500) -> str:
        """
        Sanitize and validate question input.
        
        Args:
            question: Raw question input
            max_length: Maximum allowed length
            
        Returns:
            Sanitized question (truncated if needed)
        """
        question = question.strip()
        if len(question) > max_length:
            return question[:max_length]
        return question
