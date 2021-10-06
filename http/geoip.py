import json
import os
import requests
from flask import Flask, request

app = Flask(__name__)

def _cache_list_to_string(cache_list):
    comma_list = ""
    for cache in cache_list.keys():
        comma_list += cache + ","
    return comma_list

def _write_json(data, fileName = '/home/GeoIP/httpUserLog.json'):
    with open(fileName,'w') as f: 
        json.dump(data, f, indent=4)

def _nearest_cache(UserIP):
    CACHE_LIST = {"stashcache.t2.ucsd.edu": "8000",
    "mwt2-stashcache.campuscluster.illinois.edu": "8000",
    "its-condor-xrootd1.syr.edu": "8000",
    "osg-kansas-city-stashcache.nrp.internet2.edu": "8000",
    "osg-chicago-stashcache.nrp.internet2.edu": "8000",
    "osg-new-york-stashcache.nrp.internet2.edu": "8000",
    "stash-cache.osg.chtc.io": "8000",
    "osg-gftp2.pace.gatech.edu": "8000",
    "dtn2-daejeon.kreonet.net": "8000",
    "osg-houston-stashcache.nrp.internet2.edu": "8000",
    "osg-sunnyvale-stashcache.nrp.internet2.edu": "8000"}

    OASIS_HOST = "oasis-replica.opensciencegrid.org"
    comma_list = _cache_list_to_string(CACHE_LIST)
    order_list_caches = requests.get("http://{}:8000/cvmfs/dwd.test/api/v1.0/geo/{}/{}".format(OASIS_HOST, UserIP, comma_list)).text
    order_list_caches = order_list_caches.split(",")
    nearest_cache = CACHE_LIST.keys()[int(order_list_caches[0])-1]
    port = CACHE_LIST.values()[int(order_list_caches[0])-1]
    return nearest_cache, port

def doAll(UserIP):
    log_path = '/home/GeoIP/httpUserLog.json'
    if not os.path.exists(log_path):
        os.mknod(log_path)
    with open(log_path,'r') as f:
        try:
            data = json.load(f)
        except:
            data = dict()        
    if UserIP in data:
        return data[UserIP]
    nearest_cache = _nearest_cache(UserIP)
    data.update({UserIP : nearest_cache})
    _write_json(data, log_path)
    return nearest_cache

@app.route('/')
def welcome():
    UserIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    nearest_cache = doAll(UserIP)
    return nearest_cache[0]

@app.route('/<path:subpath>')
def xcache_redirect(subpath):
    UserIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    nearest_cache = doAll(UserIP)
    return redirect('http://{}:{}/{}'.format(nearest_cache[0],nearest_cache[1],subpath),code=302)

if __name__ == '__main__':
    app.run()
