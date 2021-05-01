from flask import Flask, request, redirect, url_for, send_file
from flask import render_template
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from PIL import Image
from fpdf import FPDF
import os
import subprocess
import logging
import shutil

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.info("hello")

app.page_number = 1
app.thumb = 150 

@app.route('/')
def hello(name=None):
    if "action" in request.args:

        if request.args.get("action")=="scan":
            res=request.args.get("res")
            colour = ""
            if "colour" in request.args: colour = " --mode Color"
            pcom = "scanimage --format=png --resolution {}{}".format(res, colour).split(" ")
            app.logger.info(pcom)
            p = subprocess.Popen(pcom, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data, err = p.communicate()
            app.logger.info((len(data),err))
            with open(app.static_folder + "/test.png", "wb") as f:
                f.write(data)

        elif request.args.get("action")=="clear":
            app.page_number = 1
            app.logger.info("listing files")
            for f in os.listdir(app.static_folder):
                if not "test" in f:
                    app.logger.info("deleting {}".format(f))
                    os.unlink(app.static_folder + "/" + f)

        elif request.args.get("action")=="keep":
            if "test.png" in os.listdir(app.static_folder):
                testfile = app.static_folder + "/test.png"
                outputfile = app.static_folder + "/scan{:02d}.png".format(app.page_number)
                outputfilethumb = app.static_folder + "/_scan{:02}.png".format(app.page_number)
                shutil.copyfile(testfile, outputfile)
                with Image.open(outputfile) as i:
                    i2 = i.resize((app.thumb, int(app.thumb * i.height /i.width)))
                    i2.save(outputfilethumb) 
                app.logger.info("copied to {}".format("/scan{}.png".format(app.page_number)))
                app.page_number += 1

        elif request.args.get("action")=="shutdown":
            app.logger.info("bye")
            subprocess.Popen("sudo shutdown now".split(' '))

        elif request.args.get("action")=="pdf":
            pdf = FPDF()

            # imagelist is the list with all image filenames
            for image in [f for f in os.listdir(app.static_folder) if f.startswith("scan")]:
                pdf.add_page()
                pdf.image(app.static_folder + "/" + image,0,0,209,297)

            pdf.output(app.static_folder + "/out.pdf", "F")

            return send_file(app.static_folder + "/out.pdf", as_attachment=True)

        return redirect(url_for('hello'))

    return render_template('hello.html', thumbs=[f for f in os.listdir(app.static_folder) if "_scan" in f])


if __name__ == "__main__":
    app.run(debug=True)



