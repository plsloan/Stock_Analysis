from pymongo import MongoClient


connection_string = 'mongodb+srv://plsloan:Attd77Xqouk8@stockbotcluster.qgxuf.mongodb.net/StockBot?authSource=admin&replicaSet=atlas-13m5xk-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'
client = MongoClient(connection_string)
db = client.StockBot
