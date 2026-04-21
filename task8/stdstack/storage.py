from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.deconstruct import deconstructible

try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
except ImportError:
    MediaCloudinaryStorage = None


@deconstructible
class CloudinaryFallbackStorage(Storage):
    def __init__(self):
        self.local_storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL,
        )
        self.remote_storage = None

        cloudinary_config = getattr(settings, "CLOUDINARY_STORAGE", {})
        if MediaCloudinaryStorage and all(cloudinary_config.values()):
            self.remote_storage = MediaCloudinaryStorage()

    def _open(self, name, mode="rb"):
        if self.local_storage.exists(name):
            return self.local_storage._open(name, mode)
        if self.remote_storage:
            return self.remote_storage._open(name, mode)
        return self.local_storage._open(name, mode)

    def _save(self, name, content):
        if self.remote_storage:
            try:
                return self.remote_storage._save(name, content)
            except Exception:
                if hasattr(content, "seek"):
                    content.seek(0)
        return self.local_storage._save(name, content)

    def delete(self, name):
        if self.local_storage.exists(name):
            self.local_storage.delete(name)
            return
        if self.remote_storage:
            self.remote_storage.delete(name)

    def exists(self, name):
        if self.local_storage.exists(name):
            return True
        if self.remote_storage:
            return self.remote_storage.exists(name)
        return False

    def url(self, name):
        if self.local_storage.exists(name):
            return self.local_storage.url(name)
        if self.remote_storage:
            return self.remote_storage.url(name)
        return self.local_storage.url(name)

    def size(self, name):
        if self.local_storage.exists(name):
            return self.local_storage.size(name)
        if self.remote_storage:
            return self.remote_storage.size(name)
        return self.local_storage.size(name)

    def get_available_name(self, name, max_length=None):
        if self.remote_storage and hasattr(self.remote_storage, "get_available_name"):
            try:
                return self.remote_storage.get_available_name(name, max_length=max_length)
            except Exception:
                pass
        return self.local_storage.get_available_name(name, max_length=max_length)

    def path(self, name):
        return self.local_storage.path(name)
