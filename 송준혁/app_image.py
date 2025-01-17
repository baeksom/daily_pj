from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok # port를 우회해서 접속가능한 도메인을 할당
import os
from PIL import Image

app = Flask(__name__)
# run_with_ngrok(app)

'''
이미지 처리 함수
'''


def image_resize(image, width, height):
    return image.resize((int(width), int(height)))


def image_rotate(image):
    return image.transpose(Image.ROTATE_180)


def image_change_bw(image):
    return image.convert('L')


'''
플라스크
'''


@app.route('/image')
def index():
    return render_template('image.html')


@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file:
            return render_template('image.html', label="No Files")

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')
        img.save(f'static/{file.filename}')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get(
                'changed_width'), request.form.get('changed_height'))

        img.save(f'static/changed_{file.filename}')

        # 결과 리턴
        return render_template('image.html', label=file.filename)


if __name__ == '__main__':
    app.run(debug=True)
