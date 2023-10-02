from flask import Blueprint
from . import handler

primary = Blueprint('primary', __name__, url_prefix="/api/primary")

primary.add_url_rule('/new-search', view_func = handler.new_search)
primary.add_url_rule('/mind-map', view_func = handler.mind_map)
primary.add_url_rule('/image-search', view_func = handler.image_search)

handler.new_search.methods = ["GET"]
handler.mind_map.methods = ["POST"]
handler.image_search.methods = ["POST"]
