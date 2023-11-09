from functools import wraps
import os
from dotenv import load_dotenv
import json
import requests
from flask import Flask, request, jsonify
import google.generativeai as palm
import html
from flask_cors import CORS
from tinydb import TinyDB, where, Query
import jwt
import datetime
import copy

# from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
SECRET_KEY = "092b96o52v58b6vouwi2n0"
app.config["SECRET_KEY"] = SECRET_KEY


db = TinyDB("Student.json")
users = db.table("users")
posts = db.table("posts")


def generate_token(user_id):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=1),  # Token expiration time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        print(token)
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print("DATAT", data)
            kwargs["user_id"] = data["sub"]  # Pass user ID to the protected route
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return decorated


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    print("GOT DATA", data, email, password)

    User = Query()
    user = users.search(User.user_data.email == email)[0]
    print("UYUUU", user)

    if user is None or user["user_data"]["password"] != password:
        print("THI SPART", user, user["user_data"]["password"], password)
        return jsonify({"message": "Authentication failed"}), 401

    # remove password from user object and send with token
    temp = copy.deepcopy(user)
    del temp["user_data"]["password"]

    token = generate_token(user.doc_id)
    return jsonify({"token": token, "user": temp}), 200


@app.route("/register", methods=["POST"])
def addStudent():
    data = request.json
    # print(data)
    hobbies = data["personal_data"]["hobbies"]
    interests = data["personal_data"]["interests"]
    stressbusters = data["personal_data"]["stressbusters"]

    prompt = f"""
    hobbies: {hobbies}, interests: {interests}, the activities I do when I'm stressed: {stressbusters}
    Based on the above user data, analyze and provide an encouraging and appreciative user description. Please return it in this format, like this below example:
        user_description: "You're an inspiring soul with a zest for life. Your resilience and positive energy are truly remarkable."
    """
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.8,
        # The maximum length of the response
        max_output_tokens=800,
    )
    user_description = completion.result
    data["user_description"] = user_description.replace("", "")
    data["chats"] = {}
    print(data)
    users.insert(data)
    return "ok"


import uuid


@app.route("/getusers", methods=["GET"])
def getoosers():
    return users.all()


@app.route("/addPost", methods=["POST"])
def addPost():
    data = request.json
    data["id"] = str(uuid.uuid4())
    print(data)
    posts.insert(data)
    return "ok"


@app.route("/getPosts", methods=["GET"])
def getPosts():
    data = posts.all()
    return jsonify(data)


@app.route("/addComment", methods=["POST"])
def addComment():
    data = request.json
    print(data)
    postid = data["postid"]
    comment = data["comment"]
    post = posts.get(where("id") == postid)
    post["comments"].append(data)
    posts.update(post, doc_ids=[post.doc_id])
    return "ok"


load_dotenv()
api_key = os.getenv("api_key")
palm.configure(api_key=api_key)

models = [
    m for m in palm.list_models() if "generateText" in m.supported_generation_methods
]
model = models[0].name

# Chat history
# chat_history = {
#     "internal": [],
#     "visible": []
# }

HOST = "192.168.137.55:5000"
URI = f"http://{HOST}/api/v1/chat"


def run_chat(user_input, history):
    request = {
        "user_input": user_input,
        "history": history,
        "mode": "chat",
        "character": "Assistant",
        "regenerate": False,
        "_continue": False,
        "preset": "simple-1",
        "stopping_strings": ["User:"],
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()["results"][0]["history"]
        return result


# @app.route("/generate_char_description",methods=["POST"])
# def generate_char_description():
#     data = request.json()
#     hobbies =


@app.route("/getChats", methods=["POST"])
def getChats():
    data = request.json
    email = data["email"]
    User = Query()
    user = users.search(User.user_data.email == email)[0]
    user = copy.deepcopy(user)
    chats = user["chats"]
    chats = list(chats.values())
    return jsonify(chats)


@app.route("/analyzeChat", methods=["POST"])
def insights():
    chat_history = request.json.get("chat_history")
    formatted_text = ""
    for i in range(1, len(chat_history)):
        question, answer = chat_history[i]
        formatted_text += f"user: {question},\nai: {answer}\n"
    prompt = f"""
    Imagine you are a mental health therapist specializing in psychology, helping college students relieve stress and anxiety. Your task is to analyze the following conversation between the user and the assistant (where the AI acts as the mental therapist). If it's mentioned in the conversation that the user is a new user, consider that this is the first assessment. If not mentioned, assume that this is an assessment over a period of time. Based on this, calculate the cumulative product over a period of time for User Progress and provide descriptive labels for "Mental Health State," "Emotional State," and "Behavioral Patterns."

    User Progress: Track and score user well-being progression in long-term support relationships, including mood enhancement, symptom alleviation, and goal attainment.
    Please provide constant descriptive labels for the following:
    Mental Health severity: [Label, e.g., mild, moderate, severe]
    Emotional State: [Labels, e.g., happy, anxious, stressed, etc.]
    Behavioral Patterns: [Labels, e.g., healthy, self-destructive, etc.]

    Conversation:
    {formatted_text}

    Give the exact part of the conversation that made you choose these conclusions as a support document.

        """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.8,
        # The maximum length of the response
        max_output_tokens=800,
    )

    return jsonify(completion.result)


@app.route("/getColor", methods=["POST"])
def getColor():
    emotion = request.json.get("emotion")
    severity = request.json.get("severity")
    behavior = request.json.get("behavior")

    prompt = f"""
    This is a report word for emotional status or severity. Give me a color that could represent the words {emotion}, {severity}, {behavior} .

    the color can be a hex color code of the shade green -> yellow -> red, where green is positive and redis negative.
    Give the color codes as object in the same format:
    {{
        "emotion": "#00ff00",
        "severity": "#ffff00",
        "behavior": "#ff0000",
    }}
    The color Codes:"""

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.8,
        # The maximum length of the response
        max_output_tokens=200,
    )

    return jsonify(completion.result)


@app.route("/generate_books", methods=["POST"])
def generate_books():
    data = request.get_json()
    text = data.get("text", [])

    formatted_text = ""
    for i in range(1, len(text)):
        question, answer = text[i]
        formatted_text += f"qn: {question},\nans: {answer}\n"

    prompt = f"""
    {formatted_text}
    Based on the above conversation, give me three phrases by analyzing the conversation above that can be used to search for articles and books as a json list like
    {{
        "phrase": "not feeling good",
        "articles": [
          "https://www.helpguide.org/articles/depression/how-to-deal-with-feeling-down.htm",
          "https://www.psychologytoday.com/us/blog/the-athletes-way/201802/7-ways-cope-when-youre-feeling-down"
        ],
        "books": [
          "The Feeling Good Handbook: Revised and Updated",
          "When Things Fall Apart: Heart Advice for Hard Times"
        ]
    }},
    """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.8,
        max_tokens=800,
    )

    data = completion.result
    data = json.loads(data)
    book_names = []
    for item in data:
        book_names.extend(item["books"])

    book_info_list = []
    for book_name in book_names:
        book_info = get_books(book_name)
        book_info_list.append(book_info)

    return jsonify(book_info_list)


def get_books(book_name):
    resp = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book_name}")
    books = resp.json()

    for i in range(1):
        bk = books["items"][i]["volumeInfo"]
        id = books["items"][i]["id"]
        return {
            "title": bk["title"],
            "authors": bk.get("authors", []),
            "link": f"http://books.google.com/books?id={id}",
        }


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    chat_history = copy.deepcopy(data.get("history", ""))
    chat_id = data.get("chatid")
    email = data.get("email")
    print("Recivening", data.get("history", "")["visible"])

    data = run_chat(user_input, chat_history)

    # add chat to users db
    User = Query()
    user = users.search(User.user_data.email == email)[0]
    # print("UYUUU", user)
    user = copy.deepcopy(user)
    chat_history["internal"].append(data["internal"][-1])
    chat_history["visible"].append(data["visible"][-1])
    user["chats"][chat_id] = chat_history["visible"]
    print("ASJKDJASKDASJDLHASDHJASHJDASL", chat_history["visible"])
    users.update(user, doc_ids=[user.doc_id])
    # print(user_input)
    # print(chat_history)
    response = {"reply": html.unescape(data["visible"][-1][1]), "history": chat_history}
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)
