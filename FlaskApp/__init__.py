import json
import subprocess
import os

from flask import Flask, request, redirect, url_for
app = Flask(__name__)

def _run_command(command):
    """Runs the specified command, specified as a list. Returns stdout, stderr and return code                                                                         
    """
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode

def cache_list_to_string(cache_list):
    comma_list = ""
    for cache in cache_list:
        comma_list += cache + ","
    return comma_list

def nearest_cache(UserIP):

    CACHE_LIST = ["stashcache.t2.ucsd.edu", "mwt2-stashcache.campuscluster.illinois.edu",
                  "its-condor-xrootd1.syr.edu","osg-kansas-city-stashcache.nrp.internet2.edu",
                  "osg-chicago-stashcache.nrp.internet2.edu","osg-new-york-stashcache.nrp.internet2.edu",
                  "stash-cache.osg.chtc.io", "osg-gftp2.pace.gatech.edu",
                  "dtn2-daejeon.kreonet.net", "osg-houston-stashcache.nrp.internet2.edu",
                  "osg-sunnyvale-stashcache.nrp.internet2.edu"]

    OASIS_HOST = "oasis-replica.opensciencegrid.org"

    comma_list = cache_list_to_string(CACHE_LIST)
    cmd = ["curl", "http://%s:8000/cvmfs/dwd.test/api/v1.0/geo/%s/%s" % (OASIS_HOST, UserIP, comma_list)]
    (order_list_caches, stderr, errcode) = _run_command(cmd)
    order_list_caches = order_list_caches.split(",")

    nearest_cache = CACHE_LIST[int(order_list_caches[0])-1]
     
    return nearest_cache

def _check_log(UserIP):
    try:
        f = open('userLog.json','r')
        data = json.load(f)
        if UserIP in data:
            return data[UserIP]
    except:
        return

def _append_to_log(UserIP, near_cache):
    with open('userLog.json','a+') as f:
        try:
            data = json.load(f)
        except:
            data = dict()
        f.seek(0)
        data.update({UserIP : near_cache})
        json.dump(data,f)
        f.truncate()
    f.close()

def doAll(UserIP):
    check =  _check_log(UserIP)
    if check is not None:
        return check

    near_cache = nearest_cache(UserIP)
    _append_to_log(UserIP, near_cache)
    return near_cache

@app.route('/')
def welcome():
    UserIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    check =  _check_log(UserIP)
    if check is not None:
        return check

    near_cache = nearest_cache(UserIP)
    _append_to_log(UserIP, near_cache)
    return near_cache

@app.route('/<path:subpath>')
def xcache_redirect(subpath):
    UserIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    check =  _check_log(UserIP)
    if check is not None:
        return check

    near_cache = nearest_cache(UserIP)
    _append_to_log(UserIP, near_cache)
    return redirect('http://{}:8000/{}'.format(near_cache,subpath),code=302)

if __name__ == '__main__':
    app.debug = True
    app.run()
