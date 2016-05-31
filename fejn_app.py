from flask import Flask
from redis import StrictRedis
import json
redis = StrictRedis()
app = Flask(__name__)

@app.route('/')
def hello_world():
    random = redis.srandmember("words")
    if random:
        d= json.loads(random.decode(encoding='utf8'))
        return d["form"]
    else:
        return ":("