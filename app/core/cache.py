"""
Simple in-memory cache for storing invitation codes.
"""
from datetime import datetime, timedelta
import random
import string
from typing import Dict, Optional, Tuple

# In-memory cache for invitation codes: {invitation_code: (group_id, expires_at)}
invitation_cache: Dict[str, Tuple[str, datetime]] = {}

def generate_invitation_code() -> str:
    """
    Generate a random 8-digit invitation code.
    """
    return ''.join(random.choices(string.digits, k=8))

def store_invitation_code(group_id: str, expiration_minutes: int = 60 * 24) -> str:
    """
    Store an invitation code in the cache with an expiration time.
    
    Args:
        group_id: The ID of the group to invite to.
        expiration_minutes: The number of minutes until the invitation code expires (default: 24 hours).
        
    Returns:
        The generated invitation code.
    """
    # Generate a unique invitation code
    while True:
        invitation_code = generate_invitation_code()
        if invitation_code not in invitation_cache:
            break
    
    # Store the invitation code in the cache
    expires_at = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    invitation_cache[invitation_code] = (group_id, expires_at)
    
    return invitation_code

def get_group_id_by_invitation_code(invitation_code: str) -> Optional[str]:
    """
    Get the group ID associated with an invitation code.
    
    Args:
        invitation_code: The invitation code to look up.
        
    Returns:
        The group ID if the invitation code is valid, None otherwise.
    """
    if invitation_code not in invitation_cache:
        return None
    
    group_id, expires_at = invitation_cache[invitation_code]
    
    # Check if the invitation code has expired
    if datetime.utcnow() > expires_at:
        # Remove expired invitation code
        del invitation_cache[invitation_code]
        return None
    
    return group_id

def remove_invitation_code(invitation_code: str) -> None:
    """
    Remove an invitation code from the cache.
    
    Args:
        invitation_code: The invitation code to remove.
    """
    if invitation_code in invitation_cache:
        del invitation_cache[invitation_code]

def clean_expired_invitations() -> None:
    """
    Remove all expired invitation codes from the cache.
    """
    now = datetime.utcnow()
    expired_codes = [code for code, (_, expires_at) in invitation_cache.items() if now > expires_at]
    for code in expired_codes:
        del invitation_cache[code]