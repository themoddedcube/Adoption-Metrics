import json
from flask import Flask, render_template, session, Response, request
from werkzeug.utils import secure_filename
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import g
import io
from collections import OrderedDict
app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = "/upload"
    
@app.route('/')
def upload_fil():
   return render_template('index.html')
	
@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return 'failed to upload'
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      session["f"] = f.filename
      return render_template("graph-index.html")

@app.route('/bars', methods = ['GET', 'POST'])
def bars():
    if request.method == 'GET':
        return 'failed to upload'
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      session["f"] = f.filename
      return render_template("bar-index.html")
   
@app.route('/pie', methods = ['GET', 'POST'])
def pie():
    if request.method == 'GET':
        return 'failed to upload'
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      session["f"] = f.filename
      return render_template("pie-index.html")


@app.route('/graph', methods = ['GET', 'POST'])
def build_graph():
   #session.clear()
   zed = session.get("f", str)
   with open(zed,'r') as f:
    data = json.loads(f.read())
   df = pd.json_normalize(data, record_path =['clones'])
   df.rename(columns = {"count" : "normal"}, inplace=True)
   df.rename(columns = {"timestamp" : "timz"}, inplace=True) 
   
   months = []
   for x in range(len(df.timz)):
      if((df.timz[x][6:7]) is '4'):
         months.append('April, 2022')
      if((df.timz[x][6:7]) is '5'):
         months.append('May, 2022')
      if((df.timz[x][6:7]) is '6'):
         months.append('June, 2022')
      if((df.timz[x][6:7]) is '7'):
         months.append('July, 2022')
      
   #fig = Figure()
   fig, axis = plt.subplots(2)
   #axis = fig.add_subplot(1, 1, 1)
   fig.set_figheight(8.2)
   fig.set_figwidth(16.7)    
   xs = months
   ys = df.normal
   yss = df.uniques
   #axis.plot(xs, ys)
   axis[0].plot(xs, ys)
   axis[0].set_title("Regular Count")
   axis[1].plot(xs, yss, 'tab:orange')
   axis[1].set_title("Unique Count")
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)

   return Response(output.getvalue(), mimetype='image/png')

@app.route('/bar-graph', methods = ['GET', 'POST'])
def build_graph_pie():
   #session.clear()
   zed = session.get("f", str)
   with open(zed,'r') as f:
    data = json.loads(f.read())
   df = pd.json_normalize(data, record_path =['clones'])
   df.rename(columns = {"count" : "normal"}, inplace=True)
   df.rename(columns = {"timestamp" : "timz"}, inplace=True) 
   
   months = []
   for x in range(len(df.timz)):
      if((df.timz[x][6:7]) is '4'):
         months.append('April, 2022')
      if((df.timz[x][6:7]) is '5'):
         months.append('May, 2022')
      if((df.timz[x][6:7]) is '6'):
         months.append('June, 2022')
      if((df.timz[x][6:7]) is '7'):
         months.append('July, 2022')
         
   
   #fig = Figure()
   fig, axis = plt.subplots(2)
   fig.set_figheight(11.3)
   fig.set_figwidth(22)
   
   axis[0].bar(months, df.normal, )
   axis[0].set_title("Regular Count")
   #axis[0].set_title(f'{df.columns.values[0]}')
   axis[1].bar(months, df.uniques, color = 'orange', )
   axis[1].set_title("Unique Count")
   
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)

   return Response(output.getvalue(), mimetype='image/png')
   #return str(df.timz[1])[6:7]

@app.route('/pie-graph', methods = ['GET', 'POST'])
def build_pie_pie():
   #session.clear()
   zed = session.get("f", str)
   with open(zed,'r') as f:
    data = json.loads(f.read())
   df = pd.json_normalize(data, record_path =['clones'])
   df.rename(columns = {"count" : "normal"}, inplace=True)
   df.rename(columns = {"timestamp" : "timz"}, inplace=True) 
   for x in range(len(df.uniques)):
      df.uniques[x] = float(df.uniques[x])
   
   arr4normal = []
   arr4unique = []
   arr5normal = []
   arr5unique = []
   arr6normal = []
   arr6unique = []
   arr7normal = []
   arr7unique = []
   months = []
   for x in range(len(df.timz)):
      if(int(df.timz[x][6:7]) == 4):
         arr4normal.append(df.normal[x])
         arr4unique.append(df.uniques[x])
         months.append('April, 2022')
      if(int(df.timz[x][6:7]) == 5):
         arr5normal.append(df.normal[x])
         arr5unique.append(df.uniques[x])
         months.append('May, 2022')
      if(int(df.timz[x][6:7]) == 6):
         arr6normal.append(df.normal[x])
         arr6unique.append(df.uniques[x])
         months.append('June, 2022')
      if(int(df.timz[x][6:7]) == 7):
         arr7normal.append(df.normal[x])
         arr7unique.append(df.uniques[x])
         months.append('July, 2022')
   months = list(OrderedDict.fromkeys(months))
         
   normal = []
   uniques = []
   normal.append(sum(arr4normal))
   uniques.append(sum(arr4unique))
   normal.append(sum(arr5normal))
   uniques.append(sum(arr5unique))
   normal.append(sum(arr6normal))
   uniques.append(sum(arr6unique))
   normal.append(sum(arr7normal))
   uniques.append(sum(arr7unique))
   
   zata = {'normal': normal,
        'uniques': uniques,
         'months': months}
   
   dafa = pd.DataFrame(zata)
   
   #fig = Figure()
   fig, axis = plt.subplots(2)
   fig.set_figheight(10.8)
   fig.set_figwidth(21)
   
   axis[0].pie(dafa.normal, labels = months, autopct='%1.1f%%',)
   axis[0].set_title("Regular Count")
   axis[1].pie(dafa.uniques, labels = months, autopct='%1.1f%%',)
   axis[1].set_title("Unique Count")
   
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)

   return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
   app.run(debug = True)
   