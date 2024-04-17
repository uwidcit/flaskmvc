from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

apiKey = 'AIzaSyAa3sah23VK9X4r0hxsC4xHvWTUeLurpv8'
youtube = build('youtube', 'v3', developerKey=apiKey)

class Video:
    def __init__(self, title, image_url, video_url, description, video_id):
        self.title = title
        self.image_url = image_url
        self.video_url = video_url
        self.description = description
        self.video_id = video_id


def get_video_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def search_by_keyword(api_key, keyword, max_results):
    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        request = youtube.search().list(
            part="id,snippet",
            q=keyword,
            maxResults=max_results
        )
        response = request.execute()
        videos = []
        if "items" in response:
            for item in response["items"]:
                if item["id"].get("kind") == "youtube#video":
                    video_id = item["id"]["videoId"]
                    video_url = get_video_url(video_id)
                    title = item["snippet"]["title"]
                    image = item["snippet"]["thumbnails"]["default"]["url"]
                    description = item["snippet"]["description"]
                    video = Video(title, image, video_url, description, video_id)
                    videos.append(video)
                else:
                    print("This item is not a video.")
        else:
            print("No videos found.")

    except HttpError as e:
        print("An HTTP error occurred:")
        print(e.content)

    return videos

def home():
    videos = search_by_keyword("AIzaSyAa3sah23VK9X4r0hxsC4xHvWTUeLurpv8", "fitness", 30)
    print(videos)

home()



