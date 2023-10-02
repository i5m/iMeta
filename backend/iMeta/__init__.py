from flask import Flask
from iMeta.config import Config


def create_app(config_class = Config, **kwargs):

    app = Flask(__name__)
    app.config.from_object(Config)

    # mongo_db = MongoDBGear()
    # mongo_db = mongo_db.client.fpdb
    # FirebaseGear()


    from iMeta.routes.primary import primary
    app.register_blueprint(primary)


    return app

