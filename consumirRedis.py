import redis
ip_redis = '35.239.110.78'
redis_entidades = redis.Redis(
    host='35.239.110.78',
    port=6379,
    password='fVj1HjMcLYXE',
    db=1)
redis_entidades.rpush("kevinp",{'name': 'kevin','age':22})
a=redis_entidades.lrange("kevinp", 0, -1)
print(a)
