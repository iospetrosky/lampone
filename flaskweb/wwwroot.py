from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)
 
@app.route("/")
def index():
    return "<html><body><h1>Test site running under Flask</h1></body></html>"

@app.route("/xmas")
def xmas():
    data=['']
    return render_template('xmasmenu.html',data=data)
    
@app.route('/xmas/<light>/<mode>')
def light_action(light, mode):
    data = {'light': light,
            'mode': mode,
            'stamp': datetime.timestamp(datetime.now())}
    json.dump(data, open("/home/pi/WWW/lampone/lights.json","w"))
    data=[light + " set to " + mode]
    return render_template('xmasmenu.html',data=data)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    
    
    
#some examples of urls
#@app.route('/user/&lt;username&gt;')
#def show_user(username):
#    # show the user profile for that user
#    return 'User %s' % username
 
#@app.route('/post/&lt;int:post_id&gt;')
#def show_post(post_id):
#    # show the post with the given id, the id is an integer
#    return 'Post %d' % post_id
  