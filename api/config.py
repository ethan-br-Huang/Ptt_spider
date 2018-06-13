import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "2497533DC71EA22D7D23F5B2BF75CBA65CCEEC6308D4A376034D269D75BA6F16"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/api.db".format(os.getcwd())


config = {
    'development': DevelopmentConfig
}
