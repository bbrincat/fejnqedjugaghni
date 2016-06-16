from flask import Flask, render_template
from redis import StrictRedis
import json
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
        # print(d)
        # return d["form"]

@app.route('/')
def hello_world():
     phrase, word = generate_phrase()
     return render_template('fejn.html', phrase=phrase, word=word)

def generate_phrase():
    word_info = get_random_word()

    word = word_info["form"]
    verb =  conjugate(word_info["number"],word_info["gender"])
    article,lehen = get_article(word)

    return "qed {} {}".format(verb,article), lehen+word


@app.route('/phrase')
def phrase():
    phrase, word = generate_phrase()
    return json.dumps({"phrase": phrase, "word":word})

if __name__ == "__main__":
    app.run(debug=True)