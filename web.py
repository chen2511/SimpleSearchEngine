# coding:utf-8
from flask import Flask, request, render_template, redirect, url_for
# 本人写的 搜索引擎： import as SE
import search as SE

app = Flask(__name__, static_url_path='')
 
 
@app.route("/", methods=['POST', 'GET'])
def mainpage():
    if request.method == 'POST' and request.form.get('inputs'):
        inputs = request.form['inputs']
        
        return redirect(url_for('search', inputs=inputs))
 
    return render_template('index.html')
 
 

@app.route("/search/<inputs>", methods=['POST', 'GET'])
def search(inputs):
    results = SE.search(inputs)

    highlight_results = highlight(results, inputs)
    return render_template('search.html', results=highlight_results, value=inputs, length=len(results))
 
 
def highlight(results, inputs):
    highlight_results = []

    for result in results:
        title = result[0].replace(inputs, '<em><font color="red">{}</font></em>'.format(inputs))
        
        highlight_results.append([title, result[1], result[2]])
        
    return highlight_results
 

 
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)