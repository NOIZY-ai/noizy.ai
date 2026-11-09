#!/usr/bin/env python3
"""
================================================================================
█▀▀▀ █▀▀█ █▀▀▄ █▀▀█ ░▀░ █▀▀ █░░   █▀▀▄ █▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█
█░▀█ █▄▄█ █▀▀▄ █▄▄▀ ▀█▀ █▀▀ █░░   █▀▀▄ █▄▄▀ █░░█ █▄▄█ █░░█ █░░ █▄▄█ ▀▀█ ░░█░░ █▀▀ █▄▄▀
▀▀▀▀ ▀░░▀ ▀▀▀░ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀   ▀▀▀░ ▀░▀▀ ▀▀▀▀ ▀░░▀ ▀▀▀░ ▀▀▀ ▀░░▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀░▀▀
================================================================================
GABRIEL BROADCASTER - YOUTUBE INTEGRATION WITH IDENTITY INTERLOCK
================================================================================
FEATURES:
  ◆ OAuth2 Authentication
  ◆ Identity Verification Interlock (prevents wrong-account broadcasts)
  ◆ Live Chat Monitoring
  ◆ Comment Moderation with AI
  ◆ Broadcast Status Updates
================================================================================
"""

import os
import json
import pickle
from datetime import datetime
from pathlib import Path

# Google API imports (install: pip install google-api-python-client google-auth-oauthlib)
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("⚠️ Google API not installed. Run: pip install google-api-python-client google-auth-oauthlib")

# Import our configuration
import gabriel_config

# ==============================================================================
# CONSTANTS
# ==============================================================================
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]
TOKEN_FILE = Path(gabriel_config.PATHS.get("PORTAL", ".")) / "youtube_token.pickle"
CLIENT_SECRETS_FILE = Path(gabriel_config.PATHS.get("PORTAL", ".")) / "client_secrets.json"

# ==============================================================================
# GABRIEL BROADCASTER CLASS
# ==============================================================================
class GabrielBroadcaster:
    """
    YouTube Broadcaster with Identity Verification Interlock.
    Ensures Gabriel only broadcasts on the configured channel.
    """
    
    def __init__(self):
        print("=" * 60)
        print("📡 INITIALIZING GABRIEL BROADCAST MODULE...")
        print("=" * 60)
        
        if not GOOGLE_API_AVAILABLE:
            raise RuntimeError("Google API libraries not installed")
        
        self.credentials = self._get_credentials()
        self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=self.credentials)
        
        # 🛡️ IDENTITY VERIFICATION INTERLOCK
        self._verify_identity()
        
        print("✅ BROADCAST MODULE READY")
        print("=" * 60)
    
    def _get_credentials(self):
        """
        Get or refresh OAuth2 credentials.
        """
        print("🔑 LOADING CREDENTIALS...")
        creds = None
        
        # Load existing token
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 REFRESHING TOKEN...")
                creds.refresh(Request())
            else:
                if not CLIENT_SECRETS_FILE.exists():
                    raise FileNotFoundError(
                        f"❌ client_secrets.json not found at {CLIENT_SECRETS_FILE}\n"
                        "   Download from Google Cloud Console > APIs & Services > Credentials"
                    )
                print("🆕 INITIATING NEW AUTHENTICATION...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CLIENT_SECRETS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=8097)
            
            # Save credentials
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            print("💾 TOKEN SAVED")
        
        print("✅ CREDENTIALS LOADED")
        return creds
    
    def _verify_identity(self):
        """
        🛡️ IDENTITY VERIFICATION INTERLOCK
        Safety Check: Ensures the OAuth token matches the Configured Channel ID.
        Prevents Gabriel from broadcasting on the wrong account.
        """
        print("🛡️ VERIFYING CHANNEL IDENTITY...")
        
        try:
            response = self.youtube.channels().list(
                mine=True,
                part='id,snippet'
            ).execute()
            
            if not response.get('items'):
                print("❌ NO CHANNEL FOUND FOR THIS ACCOUNT")
                print("❌ SYSTEM HALT. PLEASE CHECK YOUR OAUTH CREDENTIALS.")
                exit(1)
            
            active_id = response['items'][0]['id']
            active_name = response['items'][0]['snippet']['title']
            config_id = gabriel_config.YOUTUBE_IDENTITY["CHANNEL_ID"]
            
            print(f"   Active Channel:  {active_name} ({active_id})")
            print(f"   Configured ID:   {config_id}")
            
            if active_id == config_id:
                print(f"✅ IDENTITY CONFIRMED: Connected to Channel {active_id}")
            elif config_id == "PASTE_CHANNEL_ID_HERE":
                print("⚠️  CONFIG NOT SET: Please update gabriel_config.py with your Channel ID")
                print(f"   Your Channel ID is: {active_id}")
                print("   Copy this to YOUTUBE_IDENTITY['CHANNEL_ID']")
            else:
                print(f"⚠️ IDENTITY MISMATCH!")
                print(f"   Configured: {config_id}")
                print(f"   Logged In:  {active_id}")
                print("❌ SYSTEM HALT. PLEASE RE-AUTHENTICATE.")
                exit(1)  # Kill process to prevent accidents
                
        except Exception as e:
            print(f"❌ IDENTITY VERIFICATION FAILED: {e}")
            raise
    
    # ==========================================================================
    # BROADCAST OPERATIONS
    # ==========================================================================
    
    def get_live_broadcasts(self):
        """Get active live broadcasts."""
        print("📺 FETCHING LIVE BROADCASTS...")
        
        response = self.youtube.liveBroadcasts().list(
            part='id,snippet,status',
            broadcastStatus='active'
        ).execute()
        
        broadcasts = response.get('items', [])
        print(f"   Found {len(broadcasts)} active broadcast(s)")
        return broadcasts
    
    def get_live_chat_id(self, broadcast_id: str) -> str:
        """Get the live chat ID for a broadcast."""
        response = self.youtube.liveBroadcasts().list(
            part='snippet',
            id=broadcast_id
        ).execute()
        
        if response.get('items'):
            return response['items'][0]['snippet'].get('liveChatId')
        return None
    
    def get_chat_messages(self, live_chat_id: str, page_token: str = None):
        """Get messages from a live chat."""
        print(f"💬 FETCHING CHAT MESSAGES...")
        
        params = {
            'liveChatId': live_chat_id,
            'part': 'id,snippet,authorDetails'
        }
        if page_token:
            params['pageToken'] = page_token
        
        response = self.youtube.liveChatMessages().list(**params).execute()
        
        messages = response.get('items', [])
        next_page = response.get('nextPageToken')
        poll_interval = response.get('pollingIntervalMillis', 5000)
        
        print(f"   Received {len(messages)} message(s)")
        return messages, next_page, poll_interval
    
    def send_chat_message(self, live_chat_id: str, message: str):
        """Send a message to live chat as Gabriel."""
        print(f"📤 SENDING MESSAGE: {message[:50]}...")
        
        body = {
            'snippet': {
                'liveChatId': live_chat_id,
                'type': 'textMessageEvent',
                'textMessageDetails': {
                    'messageText': message
                }
            }
        }
        
        response = self.youtube.liveChatMessages().insert(
            part='snippet',
            body=body
        ).execute()
        
        print("✅ MESSAGE SENT")
        return response
    
    def moderate_message(self, message_text: str) -> bool:
        """
        Check if a message should be moderated.
        Returns True if message is OK, False if should be blocked.
        """
        threshold = gabriel_config.YOUTUBE_IDENTITY.get("MODERATION_THRESHOLD", 0.85)
        
        # Basic moderation (expand with AI in production)
        blocked_patterns = ['spam', 'scam', 'http://', 'https://']
        message_lower = message_text.lower()
        
        for pattern in blocked_patterns:
            if pattern in message_lower:
                print(f"⚠️ MODERATION: Blocked pattern '{pattern}' detected")
                return False
        
        return True
    
    def delete_chat_message(self, message_id: str):
        """Delete a chat message (requires moderator permissions)."""
        print(f"🗑️ DELETING MESSAGE: {message_id}")
        
        self.youtube.liveChatMessages().delete(id=message_id).execute()
        print("✅ MESSAGE DELETED")
    
    # ==========================================================================
    # CHANNEL OPERATIONS
    # ==========================================================================
    
    def get_channel_info(self):
        """Get current channel information."""
        response = self.youtube.channels().list(
            mine=True,
            part='id,snippet,statistics'
        ).execute()
        
        if response.get('items'):
            channel = response['items'][0]
            return {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'description': channel['snippet']['description'],
                'subscribers': channel['statistics'].get('subscriberCount', 0),
                'views': channel['statistics'].get('viewCount', 0),
                'videos': channel['statistics'].get('videoCount', 0)
            }
        return None
    
    def get_recent_comments(self, video_id: str = None, max_results: int = 20):
        """Get recent comments on channel or specific video."""
        print("💬 FETCHING RECENT COMMENTS...")
        
        params = {
            'part': 'id,snippet',
            'maxResults': max_results,
            'order': 'time'
        }
        
        if video_id:
            params['videoId'] = video_id
        else:
            params['allThreadsRelatedToChannelId'] = gabriel_config.YOUTUBE_IDENTITY["CHANNEL_ID"]
        
        response = self.youtube.commentThreads().list(**params).execute()
        
        comments = []
        for item in response.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'id': item['id'],
                'author': snippet['authorDisplayName'],
                'text': snippet['textDisplay'],
                'published': snippet['publishedAt']
            })
        
        print(f"   Found {len(comments)} comment(s)")
        return comments
    
    def reply_to_comment(self, parent_id: str, message: str):
        """Reply to a comment as Gabriel."""
        broadcast_name = gabriel_config.YOUTUBE_IDENTITY.get("BROADCAST_NAME", "Gabriel [AI]")
        
        print(f"💬 REPLYING AS {broadcast_name}...")
        
        body = {
            'snippet': {
                'parentId': parent_id,
                'textOriginal': message
            }
        }
        
        response = self.youtube.comments().insert(
            part='snippet',
            body=body
        ).execute()
        
        print("✅ REPLY POSTED")
        return response


# ==============================================================================
# STANDALONE TEST
# ==============================================================================
def main():
    """Test the broadcaster module."""
    print("=" * 60)
    print("GABRIEL BROADCASTER - TEST MODE")
    print("=" * 60)
    
    try:
        broadcaster = GabrielBroadcaster()
        
        # Get channel info
        info = broadcaster.get_channel_info()
        if info:
            print(f"\n📺 CHANNEL: {info['title']}")
            print(f"   Subscribers: {info['subscribers']}")
            print(f"   Total Views: {info['views']}")
            print(f"   Videos: {info['videos']}")
        
        # Check for live broadcasts
        broadcasts = broadcaster.get_live_broadcasts()
        if broadcasts:
            print(f"\n🔴 LIVE NOW: {broadcasts[0]['snippet']['title']}")
        else:
            print("\n📴 No active broadcasts")
        
        print("\n✅ BROADCASTER TEST COMPLETE")
        
    except FileNotFoundError as e:
        print(f"\n❌ Setup Required: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
