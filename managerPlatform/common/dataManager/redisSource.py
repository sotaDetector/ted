import redis
# 拿到一个redis的连接池
Pool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=10)

# 从池子中拿一个链接
redisPool = redis.Redis(connection_pool=Pool,decode_responses = True)
