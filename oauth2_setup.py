from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly', 'https://www.googleapis.com/auth/youtube.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtubeAnalytics', 'v2', credentials=credentials), build('youtube', 'v3', credentials=credentials)

if __name__ == '__main__':
    youtube_analytics, youtube = get_authenticated_service()
    print("YouTube Analytics API и YouTube Data API настроены и готовы к использованию")
