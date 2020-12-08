import redis
# 拿到一个redis的连接池
from managerPlatform.common.config.configUtils import configUtils

Pool = redis.ConnectionPool(host=configUtils.getConfigProperties("redis","redisIp"),
                            port=int(configUtils.getConfigProperties("redis","redisPort")),
                            password=configUtils.getConfigProperties("redis","redisPass"),
                            max_connections=10)

# 从池子中拿一个链接
redisPool = redis.Redis(connection_pool=Pool,decode_responses = True,health_check_interval=30)
