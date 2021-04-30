from flask import Flask, request
from flask import render_template
app = Flask(__name__)

import os
import subprocess
import logging
import shutil

app.logger.info("hello")

app.page_number = 1

@app.route('/')
def hello(name=None):
    if "action" in request.args:
        if request.args.get("action")=="scan":
            res=request.args.get("res")
            colour = ""
            if "colour" in request.args: colour = " --color=Color"
            with open(app.static_folder + "/test.png") as f:
                p = subprocess.Popen("scanimage --format=png --resolution {}{}".format(res,colour).split(' '), shell=True, stdout=f, stderr=subprocess.PIPE)
                app.logger.info(p.communicate())

        elif request.args.get("action")=="clear":
            app.page_number = 1
            app.logger.info("listing files")
            for f in os.listdir(app.static_folder):
                if not "test" in f:
                    app.logger.info("deleting {}".format(f))
                    os.unlink(app.static_folder + "/" + f)

        elif request.args.get("action")=="keep":
            if "test.png" in os.listdir(app.static_folder):
                shutil.copyfile(app.static_folder + "/test.png", app.static_folder + "/scan{}.png".format(app.page_number))
                app.logger.info("copied to {}".format("/scan{}.png".format(app.page_number)))
                app.page_number += 1

    return render_template('hello.html')


if __name__ == "__main__":
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
