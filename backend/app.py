import os
from flaskr import create_app

os.environ['FLASK_APP'] = 'flaskr:create_app'
os.environ['FLASK_ENV'] = 'development'

app = create_app()

if __name__ == '__main__':
    app.run()