from flask import render_template
from flask import request
from flask import Flask, url_for

#from flask_sockets import Sockets
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
app.config['SECRET_KEY'] = 'secret123456789'
socketio = SocketIO(app)




#global 

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])




@app.route('/' )
def hello():
    #return "hello"
    #print(10)

##    @socketio.on('connect')
##    def on_connect():
##        payload = dict(data='Connected wahib good job')
##        emit('log', payload, broadcast=True)

    return render_template('index.html' ) 






@socketio.on('my event', namespace='/test')
def handle_message(data):
    #print(data)
    image_b64 = data['data']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    im = Image.open(BytesIO(base64.b64decode(image_data))) 
    im.save('image1.png', 'PNG')

    
    im = im.convert("RGB")

    #print(max(np.array(im)))

    im=np.array(im)
    #im=im.resize(28,28)
    gray = rgb2gray(im)
    #print(gray.shape)
    gray = cv2.resize(gray,(28,28))

    model = load_model("written.h5")
    
    #predict = model.predict(np.array(im).reshape(1,28,28))
    #predict = np.argmax(predict)

    #@socketio.on('connect')
    #def on_connect():
        #payload = dict(data='wahib good job' )
        #emit('log', payload, broadcast=True)

    payload = dict(data= str( np.argmax(model.predict(gray.reshape(1,28,28)))  ))
    #payload = dict(data= str(np.array(im).resize(28,28).shape)+'wahib good job' )

    emit('log', payload, broadcast=True)
    




#to send message




    
    
        




@app.route('/hook', methods=['POST'])
def get_image():
    
    
    image_b64 = request.values['imageBase64']
##
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)

      

    im = Image.open(BytesIO(base64.b64decode(image_data))) 
    im.save('image.png', 'PNG')
  

      
       
      #f = open("demofile.txt", "a")
      #f.write(image_data)
      #f.close()
    print(9)
    return render_template('e.html', value="9")

      



@app.route('/echo_test', methods=['GET'])
def echo_test(ws):
    ws.send(message[::-1])
    



#app.run(debug=True)
socketio.run(app,debug=True)



#   http://127.0.0.1:5000/









