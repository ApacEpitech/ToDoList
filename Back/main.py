from users import *
from tasks import *


@app.route('/')
def run():
    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0')
