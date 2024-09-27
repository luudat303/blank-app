import redisClient


sentinels =   [
    ("192.9.227.187", 26379),
    ("192.9.249.217", 26379)
    ] 
password = "MpDHeaNz1k6ZUrXv"
service_name="ntamaster"
db=0 
redis_client= redisClient.redisSentinelHelper(sentinel_list=sentinels,service_name=service_name,password=password,db=db)
