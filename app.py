from flask import render_template
from app_routines import create_app


app = create_app()


@app.route('/')
def hello_world():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(
        host=app.config['FLASK_SERVER_NAME'],
        port=app.config['FLASK_RUN_PORT'],
        debug=app.config['FLASK_DEBUG']
    )
