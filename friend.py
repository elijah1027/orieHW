import re
import sys
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
user_friend = lines.map(lambda l:tuple(l.split('\t')))
user_ratingprod = user_friend.flatMap(lambda x:[((x[0],i),0) for i in x[1].split(',')])
u_friend = user_friend.map(lambda x:(x[1].split(',')))
#print('step1')
user_ratingprod2 = user_friend.flatMap(lambda x: (lambda j:[[((j[u],j[i]),1) for i in range(u+1,len(j))]for u in range(0,len(j))])(x[1].split(',')))
user_ratingprod2 = user_ratingprod2.flatMap(lambda xs: [x for x in xs])
#print('step2')
unio = user_ratingprod.union(user_ratingprod2).reduceByKey(lambda n1,n2:n1+n2).map(lambda x: (x[0][0],(x[0][0],x[0][1],x[1])))
result = unio.filter(lambda u:u[1][2] >= 0).groupByKey().map(lambda v: sorted(v[1], key=lambda k: k[2], reverse=True)).map(lambda x: x[0:10])
result.saveAsTextFile(sys.argv[2])
sc.stop()

#~/opt/spark/bin/spark-submit friend.py soc-data.txt ~/spark_code/result/
