from src.content_item import ContentItem
from src.content_manager import ContentManager

def main():
    manager = ContentManager()
    manager.publisher.connect_to_platforms()

    # Example usage
    content1 = ContentItem("My First Post", "Check out this awesome content!", "/path/to/file1.mp4")
    content2 = ContentItem("Another Great Post", "More amazing content here!", "/path/to/file2.mp4")

    manager.add_content(content1)
    manager.add_content(content2)

    manager.publish_all()
    manager.interact_on_all_platforms()
    manager.change_profile_picture_on_all_platforms("/path/to/new_profile_pic.jpg")

if __name__ == "__main__":
    main()