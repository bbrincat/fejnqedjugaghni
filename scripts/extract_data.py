from pymongo import MongoClient
import json
from redis import StrictRedis
redis = StrictRedis()

# get only nouns, and leave out verb derived nouns
select = {"pos": "NOUN", "form": {"$ne": "verbalnoun"}}

# join lexeme and  wordform collections
query = [
    {
        "$match": select
    },
    {
        "$lookup": {
            "from": "wordforms",
            "localField": "_id",
            "foreignField": "lexeme_id",
            "as": "wf"
        }
    }
]

def word_details():
    client = MongoClient()
    lex = client.gabra.lexemes

    cursor = lex.aggregate(query)

    for lexeme in cursor:
        for wordform in lexeme['wf']:
            if not wordform.get("number"):
                continue
            yield {"gender": wordform.get("gender"),
                   "number": wordform.get("number"),
                   "form": wordform.get("surface_form"),
                   "gloss": lexeme.get("gloss"),
                   "lemma": lexeme.get("lemma")
                   }


def write_to_mongo():
    client = MongoClient()
    db = client.gabra
    db.drop_collection("kliem")
    db.create_collection("kliem")
    db.lexemes.drop_indexes()
    for word in word_details():
        db.kliem.insert({k: v for k, v in word.items() if v})


def write_to_redis():
    redis.delete("words")
    for word in word_details():
        redis.sadd("words", json.dumps(word))


if __name__ == "__main__":
    write_to_redis()
