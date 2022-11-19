from flask import Flask

# from applications.api.analysis import analysis_api
from applications.api.file import file_api
# from applications.api.history import history_api
from applications.api.model import model_api
from applications.api.myfunction import myfunction


def system_api(app: Flask):
    app.register_blueprint(file_api)
    # app.register_blueprint(history_api)
    app.register_blueprint(myfunction)
    app.register_blueprint(model_api)
    pass
