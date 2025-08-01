"""
This file contains the blocklist for JWT tokens. 
It will be imported by app and the logout resource so that tokens can be added to the blocklist when a user logs out.
"""

BLOCKLIST = set()