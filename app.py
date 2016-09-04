from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('userinfo.html')
    else:
        stock = request.form['stockticker']
    return render_template('graph.html',stockticker=stock)

if __name__ == '__main__':
  app.run(port=33507)
