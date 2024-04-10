from flask import Flask, render_template, request, redirect, url_for, flash, send_file,send_from_directory, abort
from flask_bootstrap import Bootstrap
import os, re



from func.MSBR import main as MSBR
from func.VSBR import main as VSBR
from func.output import create_output
from func.randomizer import create_new as Token

app = Flask(__name__)
bootstrap = Bootstrap(app)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['DOWNLOADS'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


app.secret_key = 'supersecretkey'


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        choice = request.form.get('choice')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            f_filename = f"{Token()}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_filename))
            if choice == "MSBR":
                oName = re.sub('txt','xlsx', f_filename)
                create_output(MSBR(f_filename), oName)
                return send_from_directory(app.config["DOWNLOADS"], oName)
            else:
                oName = re.sub('txt','xlsx', f_filename)
                create_output(VSBR(f"./uploads/{f_filename}"),oName )
                return send_from_directory(app.config["DOWNLOADS"], oName)
                
            # flash('File uploaded successfully')
            # return redirect(url_for('index'))
        else:
            flash('File type not allowed')
            return redirect(request.url)
    
    # Get list of uploaded files
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return render_template('index.html', uploaded_files=uploaded_files)

attachments_dir = './outputs/'

@app.route('/download_attachment/<path:filename>')
def download_attachment(filename):
    try:
        return send_from_directory(attachments_dir, filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
    
    print(os.listdir(attachments_dir))


if __name__ == '__main__':
    app.run(debug=True)
