from typing import List
from content_item import ContentItem
from content_publisher import ContentPublisher

class ContentManager:
    def __init__(self):
        self.content_queue: List[ContentItem] = []
        self.publisher = ContentPublisher()

    def add_content(self, content: ContentItem):
        self.content_queue.append(content)

    def publish_all(self):
        for content in self.content_queue:
            for platform in self.publisher.platforms:
                self.publisher.publish_to_platform(platform, content)
        self.content_queue.clear()

    def interact_on_all_platforms(self):
        for platform in self.publisher.platforms:
            self.publisher.interact_on_platform(platform)

    def change_profile_picture_on_all_platforms(self, image_path: str):
        for platform in self.publisher.platforms:
            self.publisher.change_profile_picture_on_platform(platform, image_path)