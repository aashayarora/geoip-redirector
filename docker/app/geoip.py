import json
import requests
from flask import Flask, request, redirect

from os import environ as env
import sqlalchemy as db

# Utility functions
def _cache_list_to_string(cache_list):
    return ",".join(cache_list)

def getClosestCacheFromIP(userIP):
    caches = json.load(open("/home/aaarora/projects/geoip-redirector/docker/app/caches_http.json"))
    cache_list = list(caches.keys())
    order_list_caches = requests.get(f"http://oasis-replica.opensciencegrid.org:8000/cvmfs/dwd.test/api/v1.0/geo/{userIP}/{_cache_list_to_string(cache_list)}").text.strip("\n")
    order_list_caches = order_list_caches.split(",")
    nearest_cache = cache_list[int(order_list_caches[0])-1]
    return f"{nearest_cache}:{caches[nearest_cache]}"

# db utility functions
def initDatabase(meta, engine):
    db.Table(
        "GeoIP" , meta,
        db.Column('UserIP', db.String(16)),
        db.Column('ClosestCache', db.String(255))
    )
    meta.create_all(engine)

def getFromDB(engine, userIP):
    geoip = db.Table('GeoIP', metadata, autoload=True, autoload_with=engine)
    query = db.select(geoip.c.ClosestCache).where(geoip.c.UserIP == userIP)
    result = engine.connect().execute(query)
    return result.fetchone()[0]

def updateDB(engine, userIP, closestCache):
    geoip = db.Table('GeoIP', metadata, autoload=True, autoload_with=engine)
    query = geoip.insert().values(UserIP=userIP, ClosestCache=closestCache)
    engine.connect().execute(query)

def getClosestCache(userIP):
    try:
        closest_cache = getFromDB(db_engine, userIP)
    except:
        closest_cache = getClosestCacheFromIP(userIP)
        updateDB(db_engine, userIP, closest_cache)
    finally:
        return closest_cache

# db initialization
hostname = env.get("DB_ADDR")
port = env.get("DB_PORT")
user = env.get("DB_USER")
password = env.get("DB_PASSWD")
db_name = env.get("DB_NAME")

db_engine = db.create_engine(f"mysql+mysqlconnector://{user}:{password}@{hostname}:{port}/{db_name}")
metadata = db.MetaData()

initDatabase(metadata, db_engine)

# Frontend
app = Flask(__name__)
@app.route('/<path:subpath>')
def xcache_redirect(subpath):
    userIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return redirect('http://{}/{}'.format(getClosestCache(userIP),subpath),code=302)

if __name__ == '__main__':
    app.run()