from flask import Flask, request
from flask import render_template
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

import os
import subprocess
import logging
import shutil

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
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

        elif request.args.get("action")=="shutdown":
            p = subprocess.Popen("sudo shutdown now".split(' '), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            app.logger.info(p.communicate())

    return render_template('hello.html')


if __name__ == "__main__":
    app.run(debug=True)
