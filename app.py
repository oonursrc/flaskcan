#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

indapp_sources={}

@app.route('/')
def index():
    return "Hello, World!"

  
@app.route('/source/add/indapp/<string:release_id>')
def set_indapp_source(release_id):
    global indapp_sources
    if release_id not in indapp_sources:
        indapp_sources[release_id] = []
    if str(request.remote_addr) not in indapp_sources[release_id]:
        indapp_sources[release_id].append(str(request.remote_addr))
    else:
        return "IP Already exists for this ReleaseID"
    return "IP address has been added ! "


@app.route('/source/get/indapp/<string:release_id>')
def get_indapp_source(release_id):
    global indapp_sources
    if release_id in indapp_sources:
        return jsonify({"sources": indapp_sources[release_id]}),200
    else:
        return jsonify({"sources": []}),404
      
      
@app.route('/file/get/indapp/<string:app_name>/<string:sw_id>/<string:release_id>/')
def get_indapp_file(app_name, sw_id, release_id):
    global indapp_sources
    if release_id in indapp_sources:
        cmd = 'smbget smb://' + indapp_sources[release_id][0] + '/edgeshare/' + app_name + '#' + sw_id + '#' + release_id + '.indapp --user=root%edgeshare'
        return jsonify({'cmd': cmd}), 200
    return "", 404

  
@app.route('/source/get/indapp/all')
def get_indapp_all():
  return jsonify({'source': indapp_sources}), 200

if __name__ == '__main__':
    app.run("0.0.0.0",5000)
    
    
    
    
    
    
    
    