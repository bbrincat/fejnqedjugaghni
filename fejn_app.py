from flask import Flask
from redis import StrictRedis
import json
redis = StrictRedis()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return json.loads(redis.srandmember("words")["form"])