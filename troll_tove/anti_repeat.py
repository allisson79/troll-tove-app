"""
Anti-repetition logic for Troll-Tove app.

Handles caching and rules to avoid repeated predictions for the same user.
Uses IP-based caching with timeout to ensure users get consistent predictions
within a time window.
"""
import time
import logging
from collections import OrderedDict
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class PredictionCache:
    """
    LRU Cache for IP-based predictions with timeout.
    
    Implements an LRU (Least Recently Used) cache that stores predictions
    per IP address with automatic expiration. This ensures users get the
    same prediction if they ask again within the timeout period.
    """
    
    def __init__(self, max_size: int = 1000, timeout: int = 3600):
        """
        Initialize cache with size and timeout limits.
        
        Args:
            max_size: Maximum number of entries to cache
            timeout: How long entries remain valid (seconds, default 1 hour)
        """
        self.cache = OrderedDict()
        self.max_size = max_size
        self.timeout = timeout
    
    def get(self, ip: str) -> Optional[str]:
        """
        Retrieve cached prediction for an IP address.
        
        Args:
            ip: IP address key
            
        Returns:
            Cached prediction if valid, None if expired or not found
        """
        if ip in self.cache:
            prediction, timestamp = self.cache[ip]
            # Check if cache entry is still valid
            if time.time() - timestamp < self.timeout:
                # Move to end (most recently used)
                self.cache.move_to_end(ip)
                return prediction
            else:
                # Remove expired entry
                del self.cache[ip]
        return None
    
    def set(self, ip: str, prediction: str) -> None:
        """
        Store a prediction for an IP address.
        
        Args:
            ip: IP address key
            prediction: Prediction to cache
        """
        if ip in self.cache:
            self.cache.move_to_end(ip)
        self.cache[ip] = (prediction, time.time())
        # Remove oldest if max size exceeded
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """
        Get current cache size.
        
        Returns:
            Number of entries currently in cache
        """
        return len(self.cache)
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = [
            ip for ip, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.timeout
        ]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)


class IPValidator:
    """
    Validates and normalizes IP addresses.
    
    Handles IP address extraction from headers and validation
    to ensure consistent cache keys.
    """
    
    @staticmethod
    def extract_and_validate(forwarded_for: Optional[str], remote_addr: str) -> str:
        """
        Extract and validate IP address from request.
        
        Args:
            forwarded_for: X-Forwarded-For header value
            remote_addr: Direct remote address
            
        Returns:
            Validated IP address string or "unknown"
        """
        from ipaddress import ip_address, AddressValueError
        
        try:
            # Try X-Forwarded-For first (for proxies/load balancers)
            ip_to_check = forwarded_for if forwarded_for else remote_addr
            # Handle comma-separated list in X-Forwarded-For
            if ip_to_check and "," in ip_to_check:
                ip_to_check = ip_to_check.split(",")[0].strip()
            # Validate it's a real IP address
            return str(ip_address(ip_to_check))
        except (AddressValueError, ValueError, AttributeError) as error:
            logger.warning(f"Invalid IP address: {error}")
            return "unknown"
