"""YouTube upload automation using YouTube Data API v3."""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle
from typing import Dict, Optional, List


class YouTubeUploader:
    """Upload videos to YouTube automatically."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube.force-ssl'  # Access to channel info
    ]
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    
    def __init__(
        self,
        client_secrets_file: str = "config/client_secrets.json",
        credentials_file: str = "config/credentials.pickle"
    ):
        """Initialize YouTube uploader.
        
        Args:
            client_secrets_file: Path to OAuth2 client secrets JSON
            credentials_file: Path to store credentials
        """
        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API."""
        creds = None
        
        # Load existing credentials
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.client_secrets_file):
                    raise FileNotFoundError(
                        f"Client secrets file not found: {self.client_secrets_file}\n"
                        "Please download OAuth2 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.SCOPES
                )
                # Run with access_type='offline' to get refresh token
                creds = flow.run_local_server(
                    port=0,
                    access_type='offline',
                    prompt='consent'
                )
            
            # Save credentials for next run
            with open(self.credentials_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            credentials=creds
        )
    
    def get_channel_id(self, channel_name: str = None) -> Optional[str]:
        """Get channel ID for a specific channel name.
        
        Args:
            channel_name: Name of the channel (e.g., 'explicado_shorts')
            
        Returns:
            Channel ID if found, None otherwise
        """
        try:
            # Get list of channels for the authenticated user
            channels_response = self.youtube.channels().list(
                part='snippet,contentDetails',
                mine=True
            ).execute()
            
            if not channels_response.get('items'):
                return None
            
            # If channel_name is provided, try to match
            if channel_name:
                import yaml
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'config', 'youtube_channels.yaml'
                )
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                        channel_config = config.get('channels', {}).get(channel_name, {})
                        target_id = channel_config.get('channel_id')
                        if target_id:
                            # Verify channel exists
                            for channel in channels_response['items']:
                                if channel['id'] == target_id:
                                    return target_id
            
            # Return first channel (default)
            return channels_response['items'][0]['id']
            
        except Exception as e:
            print(f"Warning: Could not get channel ID: {e}")
            return None
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public",  # private, unlisted, public
        thumbnail_path: Optional[str] = None,
        check_duplicate: bool = True,
        channel_name: str = None  # Channel identifier
    ) -> Dict:
        """Upload a video to YouTube.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: Privacy status (private, unlisted, public)
            thumbnail_path: Optional path to thumbnail image
            check_duplicate: Check if video with same title already exists
            
        Returns:
            Dictionary with video ID and URL, or None if duplicate found
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Check if video already exists
        if check_duplicate:
            existing = self.video_exists(title)
            if existing:
                print(f"⚠️  Video já existe no YouTube")
                print(f"   Título: {existing['title']}")
                print(f"   URL: {existing['url']}")
                print(f"   Status: {existing['status']}")
                return existing
        
        if tags is None:
            tags = []
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload object
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/*'
        )
        
        # Insert video
        try:
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = self._resumable_upload(insert_request)
            
            video_id = response['id']
            
            # Upload thumbnail if provided
            if thumbnail_path and os.path.exists(thumbnail_path):
                self.upload_thumbnail(video_id, thumbnail_path)
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            return {
                'video_id': video_id,
                'url': video_url,
                'title': title
            }
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise
    
    def _resumable_upload(self, insert_request):
        """Execute resumable upload."""
        response = None
        error = None
        retry = 0
        
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(f"Video uploaded successfully. Video ID: {response['id']}")
                    else:
                        raise Exception(f"Upload failed with response: {response}")
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except Exception as e:
                error = f"A non-retriable error occurred: {e}"
                raise
        
        if error is not None:
            print(f"The following error occurred: {error}")
            raise Exception(error)
        
        return response
    
    def upload_thumbnail(self, video_id: str, thumbnail_path: str):
        """Upload thumbnail for a video.
        
        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image
        """
        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError(f"Thumbnail file not found: {thumbnail_path}")
        
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            print(f"Thumbnail uploaded for video {video_id}")
        except HttpError as e:
            print(f"An HTTP error occurred while uploading thumbnail: {e}")
            raise
    
    def update_video_metadata(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """Update video metadata.
        
        Args:
            video_id: YouTube video ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)
        """
        # Get current video data
        video_response = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not video_response['items']:
            raise ValueError(f"Video {video_id} not found")
        
        video = video_response['items'][0]
        snippet = video['snippet']
        
        # Update fields
        if title:
            snippet['title'] = title
        if description:
            snippet['description'] = description
        if tags:
            snippet['tags'] = tags
        
        # Update video
        self.youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()
        
        print(f"Video {video_id} metadata updated")
    
    def video_exists(self, title: str, channel_name: str = None) -> Optional[Dict]:
        """Check if a video with the given title already exists.
        
        Args:
            title: Video title to search for
            channel_name: Optional channel name to filter search
            
        Returns:
            Dictionary with video info if found, None otherwise
        """
        try:
            # Search for videos with matching title
            search_params = {
                'q': title,
                'part': 'id,snippet',
                'type': 'video',
                'maxResults': 10,
                'forMine': True  # Only search in own channels
            }
            
            # If channel_name specified, try to filter by channel
            if channel_name:
                channel_id = self.get_channel_id(channel_name)
                if channel_id:
                    search_params['channelId'] = channel_id
            
            search_response = self.youtube.search().list(**search_params).execute()
            
            # Check if exact title match exists
            for item in search_response.get('items', []):
                if item['snippet']['title'] == title:
                    video_id = item['id']['videoId']
                    # Get full video details
                    video_response = self.youtube.videos().list(
                        part='snippet,status',
                        id=video_id
                    ).execute()
                    
                    if video_response.get('items'):
                        return {
                            'video_id': video_id,
                            'title': item['snippet']['title'],
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'status': video_response['items'][0]['status']['privacyStatus']
                        }
            
            return None
            
        except HttpError as e:
            print(f"Error checking for existing video: {e}")
            return None
