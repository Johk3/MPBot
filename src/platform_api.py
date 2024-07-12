import abc

class PlatformAPI(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def publish_content(self, content):
        pass

    @abc.abstractmethod
    def interact_with_users(self):
        pass

    @abc.abstractmethod
    def change_profile_picture(self, image_path: str):
        pass