import re
import sys
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
user_friend = lines.map(lambda l:tuple(l.split('\t')))
user_ratingprod = user_friend.flatMap(lambda x:[((x[0],i),-1000) for i in x[1].split(',')])
u_friend = user_friend.map(lambda x:(x[1].split(',')))
#print('step1')
#Reference:
#https://stackoverflow.com/questions/16857204/lambda-inside-lambda          (lambda in side lambda)
#https://stackoverflow.com/questions/29383720/python-lambda-with-double-loops   (nested loop)
user_ratingprod2 = user_friend.flatMap(lambda x: (lambda j:[[((j[u],j[i]),1) for i in range(u+1,len(j))]for u in range(0,len(j))])(x[1].split(',')))
user_ratingprod2 = user_ratingprod2.flatMap(lambda xs: [x for x in xs])
#print('step2')
#Reference:
#https://stackoverflow.com/questions/33743978/spark-union-of-multiple-rdds    (Merge two RDD)
unio = user_ratingprod.union(user_ratingprod2).reduceByKey(lambda n1,n2:n1+n2).map(lambda x: (x[0][0],(x[0][0],x[0][1],x[1])))
#Reference:
#https://stackoverflow.com/questions/35532612/how-to-filter-a-rdd-according-to-list-of-values  (RDD filter)
#https://stackoverflow.com/questions/30164865/spark-get-top-n-by-key
#https://stackoverflow.com/questions/38626124/getting-top-n-items-per-group-in-pyspark
result = unio.filter(lambda u:u[1][2] >= 0).groupByKey().map(lambda v: sorted(v[1], key=lambda k: k[2], reverse=True)).map(lambda x: x[0:10])
result.saveAsTextFile(sys.argv[2])
sc.stop()

#~/opt/spark/bin/spark-submit friend.py soc-data.txt ~/spark_code/result/
