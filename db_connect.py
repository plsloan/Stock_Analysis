from pymongo import MongoClient


# mongodb+srv://plsloan:Melbae2015!@stockbot-zv4tn.mongodb.net/test?retryWrites=true&w=majority
connection_string = 'mongodb+srv://plsloan:Melbae2015%21@stockbot-zv4tn.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient()
db = client.StockBot
