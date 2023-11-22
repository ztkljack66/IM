import pymongo


def conn_mongodb():
    try:
        client = pymongo.MongoClient('mongodb://192.168.6.70:27017')
        # client = pymongo.MongoClient('mongodb://root:123456@192.168.6.88:27017') 
        return client
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    mongo=conn_mongodb()
    data = mongo["im"]["user"].find()
    for i in data:
        print(i)
