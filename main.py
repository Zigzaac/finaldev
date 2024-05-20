import logging
import re
from aiogram import Bot, Dispatcher, executor, types
from googleapiclient.discovery import build
from analyze import analyze_comments

API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm YouTube Comment Analyzer Bot. Send me a YouTube video link to get started.")

@dp.message_handler(regexp=r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=)?([^\s&]+)')
async def handle_video_link(message: types.Message):
    video_url = message.text
    video_id = re.findall(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=)?([^\s&]+)', video_url)[0][-1]
    comments = get_video_comments(video_id)
    
    if not comments:
        await message.reply("No comments found for this video.")
        return

    sentiments, most_positive_comment, most_negative_comment = analyze_comments(comments)
    
    response = (
        f"Analyzing comments for video ID: {video_id}\n\n"
        f"Sentiment Analysis:\n"
        f"Positive: {sentiments['positive']}\n"
        f"Negative: {sentiments['negative']}\n"
        f"Neutral: {sentiments['neutral']}\n\n"
        f"Most Positive Comment: {most_positive_comment}\n\n"
        f"Most Negative Comment: {most_negative_comment}\n"
    )

    await message.reply(response)

def get_video_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while request is not None:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)
    
    return comments

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
