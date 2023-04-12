from flask import Flask, render_template, request, send_file, redirect, url_for, copy_current_request_context
from werkzeug.utils import secure_filename
from fileinput import filename
import openai
import pyperclip as pc 

openai.api_key = "apikey"
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)

@app.route('/upload', methods=["Get", "Post"])
def upload_file():
    output = ""
    if (request.method == 'POST' and request.form.get("input") != ""):
        text = str(request.form.get("input"))
        percentage = int(request.form.get("words"))
        txt = text.split(" ")
        num_of_words = len(txt)
        to_compress = (percentage*num_of_words)/100
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'''summarise into { to_compress} \n{text}'''}])
        output = completion.choices[0].message.content

    if request.method == 'POST' and request.form.get("input") == "":
        f = request.files['file']

        f.save(secure_filename(f.filename))
        with open(f"{secure_filename(f.filename)}", "rb") as data:
            item = data.read()
            item = item.decode('utf-8', 'ignore')

        percentage = int(request.form.get("words"))
        txt = item.split(" ")
        num_of_words = len(txt)
        to_compress = (percentage*num_of_words)/100
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'''summarise into { to_compress} \n{item}'''}])
        output = completion.choices[0].message.content
    pc.copy(output)

    return render_template('uploader.html', output=output)


@app.route("/download/<output>", methods=["Get", "post"])
def download(output):
    with open("summari.txt", "w") as f:
        f.writelines(output)
        f.close()
    return send_file("summari.txt", as_attachment=True)


@app.route("/clear", methods=["Get", "post"])
def clear():
    return redirect(url_for("upload_file"))

if __name__ == '__main__':
    app.run(debug=True)
