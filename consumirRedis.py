import redis
ip_redis = '35.239.110.78'
redis_entidades = redis.Redis(
    host='35.239.110.78',
    port=6379,
    password='fVj1HjMcLYXE',
    db=1)
redis_entidades.incrby('puta', 1) 
