from flask import Blueprint
from . import get_image, put_image
from .. import restapi

image = Blueprint('image', __name__)
restapi.init_app(image)
restapi.add_resource(get_image.getImage,
                     '/getuser/<int:user_id>',
                     '/getcurrent/<int:image_number>',
                     '/getcurrent')
restapi.add_resource(put_image.putImage, '/post')
