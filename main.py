# © 2020 Wahib Mzali


from flask import render_template
from flask import request
from flask import Flask, url_for
from flask_socketio import SocketIO
from flask_socketio import send, emit
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import base64
import re
from io import StringIO
from io import BytesIO
from PIL import Image
import base64
import cv2





app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
socketio = SocketIO(app)



def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])




@app.route('/' )
def hello():
    return render_template('index.html' ) 






@socketio.on('my event', namespace='/test')
def handle_message(data):
    #print(data)
    image_b64 = data['data']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    im = Image.open(BytesIO(base64.b64decode(image_data))) 

    
    im = im.convert("RGB")

    im=np.array(im)
    gray = rgb2gray(im)
    gray = cv2.resize(gray,(28,28))

    model = load_model("model.h5")

    payload = dict(data= str( np.argmax(model.predict(gray.reshape(1,28,28)))  ))
    
    emit('log', payload, broadcast=True)
    


socketio.run(app,debug=True)


# © 2020 Wahib Mzali 






