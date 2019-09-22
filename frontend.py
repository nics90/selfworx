from flask import Flask,render_template,redirect,request,url_for,session

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
  return render_template('base.html')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
