from typing import Dict
from platform_api import PlatformAPI
from instagram_api import InstagramAPI
from youtube_api import YoutubeAPI
from content_item import ContentItem

class ContentPublisher:
    def __init__(self):
        self.platforms: Dict[str, PlatformAPI] = {
            "instagram": InstagramAPI(),
            "youtube": YoutubeAPI()
        }

    def connect_to_platforms(self):
        for platform in self.platforms.values():
            platform.connect()

    def publish_to_platform(self, platform: str, content: ContentItem):
        if platform in self.platforms:
            self.platforms[platform].publish_content(content)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    def interact_on_platform(self, platform: str):
        if platform in self.platforms:
            self.platforms[platform].interact_with_users()
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    def change_profile_picture_on_platform(self, platform: str, image_path: str):
        if platform in self.platforms:
            self.platforms[platform].change_profile_picture(image_path)
        else:
            raise ValueError(f"Unsupported platform: {platform}")