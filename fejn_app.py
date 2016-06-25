from django.shortcuts import redirect
from flask import Flask, render_template, send_from_directory, send_file
from os import path
from redis import StrictRedis
import json

from screenshot import generate_screenshot_file

redis = StrictRedis()
app = Flask(__name__)

gender_map = {
    "m": "juġagħni",
    "f": "tuġagħni"
}

def conjugate(number, gender):
    if number == "pl":
        return "juġgħuni"
    else:
        return gender_map.get(gender, gender_map.get("m"))

vowels= {"a","e","i","o", "u"}
konsonanti_lehen = {"m", "n", "r", "s", "x"}
qamrin = {"b" ,"f", "ġ","g" ,"għ", "h", "ħ" , "j" , "k" ,"l", "m" ,"p","q" ,"v", "w"}
xemxin = {"ċ","n","r","s","t","d","x","z","ż"}
ghajn  = ["g","ħ"]

def get_article(word):
    letters = list(word)

    if letters[0:2] == ghajn or letters[0] == "h" or letters[0] in vowels:
        return "l-", ""
    if letters[0] in konsonanti_lehen and letters[1] not in vowels:
        return  "l-", "i"
    if letters[0] in qamrin:
        return "il-",""
    if letters[0] in xemxin:
        return "i{}-".format(letters[0]),""
    else:
        return "l-",""

def get_random_word():
    random = redis.srandmember("words")
    if random:
        d= json.loads(random.decode(encoding='utf8'))
        return  d

def get_word_by_id():
    word_info = redis.hget("words_hash", "key")
    if word_info:
        return json.loads(word_info.decode(encoding='utf8'))


@app.route('/')
def hello_world():
    # random = redis.srandmember("words_index")
    # random = "12321323"
    # url = path.join("http://www.fejnqedjugaghni.com", "kelma", random)
    # return redirect(url)
     word_info = get_random_word()
     phrase, word, gloss = generate_phrase(word_info)
     return render_template('fejn.html', phrase=phrase, word=word, gloss=gloss)

def generate_phrase(word_info):


    word = word_info["form"]
    verb =  conjugate(word_info["number"],word_info["gender"])
    article,lehen = get_article(word)

    return "qed {} {}".format(verb,article), lehen+word, word_info["gloss"].replace("\n", "; ")


@app.route('/phrase')
def phrase():
    phrase, word, gloss = generate_phrase()
    return json.dumps({"phrase": phrase, "word":word, "gloss":gloss})


@app.route("/images/<pid>.jpg")
def get_image(pid):
    filename = path.join("static","images","{}.jpg".format(pid))
    if not (path.exists(filename) and path.isfile(filename)):
        generate_screenshot_file(filename, "http://www.fejnqedjugaghni.com", pid)
    return send_file(filename)

@app.route("/kelma/<id>")
def render_word():
    word_info = get_word_by_id(id)
    phrase, word, gloss = generate_phrase(word_info)
    return render_template('fejn.html', phrase=phrase, word=word, gloss=gloss)



if __name__ == "__main__":
    app.run(debug=True)