# reddit_api

The api is hosted on heroku.
REGISTER API: PUT request- https://easecentral-hk.herokuapp.com/api/register/
-> requires {"username":"", "password":""}

LOGIN API: POST- https://easecentral-hk.herokuapp.com/api/login/

REDDIT API: GET- https://easecentral-hk.herokuapp.com/api/reddit?access_token=afec9a1a1436478207e63c12d9a63a538001c529

FAVORITE API: PUT- https://easecentral-hk.herokuapp.com/api/favorite/
{"access_token":"afec9a1a1436478207e63c12d9a63a538001c529", "reddit_id":"7ovifj", "tags":["funny", "thriller"]}

FAVORITES API: GET - https://easecentral-hk.herokuapp.com/api/favorites?access_token=afec9a1a1436478207e63c12d9a63a538001c529

TAG API: GET- https://easecentral-hk.herokuapp.com/api/tag?access_token=afec9a1a1436478207e63c12d9a63a538001c529&tag=thriller
