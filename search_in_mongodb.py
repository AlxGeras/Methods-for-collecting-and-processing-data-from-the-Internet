from pymongo import MongoClient
from pprint import pprint

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'insta'

client = MongoClient(MONGO_URI)
mongo_base = client[MONGO_DATABASE]
collection = mongo_base['instagram']

user_id = '27850543557'

#  запрос к базе, который вернет список подписчиков только указанного пользователя

search_followers_by_id = collection.find({'user_id': user_id, 'status': 'followed'} )

for follower in search_followers_by_id:
    print(follower)


print('________________________________________________________________________________')

#  запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
search_following_by_id = collection.find({'user_id': user_id, 'status': 'following'} )

for following in search_following_by_id:
    print(following)