import redis 
from redis.sentinel import Sentinel

class redisSentinelHelper():
    def __init__(self,sentinel_list,service_name,password,db):
        self.sentinel = Sentinel(sentinel_list,socket_timeout=0.5)
        self.service_name = service_name
        self.password = password
        self.db = db

    def get_master_redis(self):
        return self.sentinel.discover_master(self.service_name)

    def get_slave_redis(self):
        return self.sentinel.discover_slaves(self.service_name)

    def set_key(self,key,value):
        master = self.sentinel.master_for(
            service_name=self.service_name,
            socket_timeout=0.5,
            password=self.password,
            db=self.db
        )
        return master.set(key,value)

    def get_key(self,key):
        slave = self.sentinel.slave_for(
            service_name=self.service_name,
            socket_timeout=0.5,
            password=self.password,
            db=self.db
        )
        return slave.get(key).decode("utf-8")
    

sentinels = [ ("192.9.227.187", 26379), ("192.9.249.217", 26379)  ] 
password = "MpDHeaNz1k6ZUrXv"
service_name="ntamaster"
db=0 

redis_cli = redisSentinelHelper(sentinel_list=sentinels,service_name=service_name,password=password,db=db)