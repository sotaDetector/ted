import redis
# 拿到一个redis的连接池
from flask_session import Session

from managerPlatform.common.config.configUtils import configUtils

Pool = redis.ConnectionPool(host=configUtils.getConfigProperties("redis", "redisIp"),
                                port=int(configUtils.getConfigProperties("redis", "redisPort")),
                                # password=configUtils.getConfigProperties("redis", "redisPass"),
                                max_connections=10)
redisClient = redis.Redis(connection_pool=Pool, decode_responses=True, health_check_interval=30)

def initRedisConfig(app):


    app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
    app.config['SESSION_PERMANENT'] = False  # 如果设置为True，则关闭浏览器session就失效。
    app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
    app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀

    app.config['SESSION_REDIS'] = redisClient # 用于连接redis的配置

    Session(app)


