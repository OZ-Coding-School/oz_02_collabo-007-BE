from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader


class ImageService:
    def __init__(self):
        self.uploader = S3ImageUploader()

    def upload_image(self, instance, image_data):
        file_url, extension, size = self.uploader.upload_file(image_data)

        image_instance = ImageUrl.objects.create(
            image_url=file_url,
            extension=extension,
            size=size
        )
        instance.image_url = image_instance
        instance.save()

    def delete_image(self, instance):
        if instance.image_url:
            image_url_instance = instance.image_url
            instance.image_url = None
            instance.save()
            image_url_instance.delete()
