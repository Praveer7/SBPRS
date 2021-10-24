
# This is basically the heart of my flask 


from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
from model import Recommendation

recommend = Recommendation()
app = Flask(__name__)  # intitialize the flaks app  # common 

@app.route('/', methods = ['POST', 'GET'])
def home():
    flag = False 
    data = ""
    if request.method == 'POST':
        flag = True
        user = request.form["userid"]
        data=recommend.getTopProducts(user)
    return render_template('index.html', data=data, flag=flag)


if __name__ == '__main__' :
    app.run(debug=True )  # this command will enable the run of your flask app or api
    
    #,host="0.0.0.0")






