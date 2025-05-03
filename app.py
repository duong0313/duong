from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MUSIC_FOLDER'] = 'static/music'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MUSIC_FOLDER'], exist_ok=True)

posts = []

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d')

        image = request.files['image']
        image_path = ''
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'uploads/{filename}'

        music = request.files['music']
        music_path = ''
        if music and music.filename != '':
            music_filename = secure_filename(music.filename)
            music.save(os.path.join(app.config['MUSIC_FOLDER'], music_filename))
            music_path = f'music/{music_filename}'

        posts.insert(0, {
            'title': title,
            'author': author,
            'date': date,
            'content': content,
            'image': image_path,
            'music': music_path
        })
        return redirect(url_for('home'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
