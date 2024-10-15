from app.models.post_image_model import ImageBase


class ImagePublic(ImageBase):
    pass


# Properties to receive on image creation
class ImageCreate(ImageBase):
    pass


# Properties to receive on image update
class ImageUpdate(ImageBase):
    pass