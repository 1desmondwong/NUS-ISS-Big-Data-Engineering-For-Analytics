from pyspark import SparkContext, SparkConf, SQLContext
conf = SparkConf().setAppName("RDD").setMaster("local[2]")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
# Create RDDs
airports = sc.textFile("airports.text")
myRDD = sc.textFile('airport-codes-na.txt')
myRDD.take(5)
myRDD.count()
sc.textFile('airport-codes-na.txt').map(lambda line: line.split("\t"))
myRDD.getNumPartitions()
myRDD = sc.textFile('airport-codes-na.txt', minPartitions=4, use_unicode=True).map(lambda line: line.split("\t"))
myRDD.take(5)
myRDD.getNumPartitions()
myRDD = sc.textFile('departuredelays.csv').map(lambda line: line.split(","))
myRDD.count()
myRDD = sc.textFile('departuredelays.csv', minPartitions=8).map(lambda line: line.split(","))
myRDD.count()
myRDD.take(5)
myRDD.getNumPartitions()
myDF = sqlContext.read.format("com.databricks.spark.csv").option("delimiter", ",").option("header", 'true').option("inferschema",'true').load("departuredelays.csv")
myDF.count()
myDF.show()
myDF.rdd.getNumPartitions()
myDF.printSchema()
# Map Example Map
lineLengths = airports.count()

# Example for map()
print(airports.map(lambda c: (c[0], c[1])).take(5))
# Example for filter()
print(airports.map(lambda c: (c[0], c[1])).filter(lambda c: c[1] == "WA").take(5))
# Example for  flatMap()
print(airports.filter(lambda c: c[1] == "WA").map(lambda c: (c[0], c[1])).flatMap(lambda x: x).take(10))
# Example for distinct()
print(airports.map(lambda c: c[2]).distinct().take(5))
# Example for sample()
flights = sc.textFile('departuredelays.csv').map(lambda line: line.split(","))
print(flights.map(lambda c: c[3]).sample(False, 0.001, 123).take(5))
# Example for leftOuterJoin()
flights.map(lambda c: (c[3], c[0])).take(5)
print(flights.take(5))
airports.map(lambda c: (c[3], c[1])).take(5)
flt = flights.map(lambda c: (c[3], c[0]))
air = airports.map(lambda c: (c[3], c[1]))
print(flt.join(air).take(5))
flt = flights.map(lambda c: (c[3], c[0]))
air = airports.map(lambda c: (c[3], c[1]))
print(flt.join(air))
# Example for repartition()
flights.getNumPartitions()
flights2 = flights.repartition(8)
flights2.getNumPartitions()
print(flights2)
