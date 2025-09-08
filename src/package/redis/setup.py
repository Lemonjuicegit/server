import redis

r = redis.Redis(host='localhost', port=45455, decode_responses=True) 
