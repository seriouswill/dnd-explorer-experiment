from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, IntegerType

spark = SparkSession.builder.appName("retail_stream").getOrCreate()

# Define the schema for our data
schema = StructType([
    StructField("store_location", StringType(), True),
    StructField("time_of_purchase", TimestampType(), True),
    StructField("product_ID", StringType(), True),
    StructField("transaction_amount", IntegerType(), True)
])

# Stream from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "retail_transactions") \
    .load()

# Deserialize the value from Kafka message
transactions = df.selectExpr("CAST(value AS STRING)").selectExpr("from_json(value, schema) as data").select("data.*")

transactions.writeStream.outputMode("append").format("console").start()