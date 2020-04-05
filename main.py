from flask import Flask
from server.index import all_server_routes
from config.ConfReader import conf

app = Flask(__name__)
app.debug = True

# entry point to all server routes
all_server_routes(app)

app.run(port=conf.PORT)
