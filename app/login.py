import app.app as app

app = Flask(__name__)
client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

@app.route('/login', methods=["POST"])
def login():
    pass