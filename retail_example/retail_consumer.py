from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, IntegerType
from pyspark.sql.functions import from_json, col

spark = SparkSession.builder.appName("WriteToTopic") \
.config("spark.jars","jars/commons-pool2-2.11.1.jar,jars/spark-sql-kafka-0-10_2.13-3.5.0.jar,jars/spark-streaming-kafka-0-10-assembly_2.12-3.4.0.jar,jars/kafka-clients-3.5.0.jar").getOrCreate()


for i in range(1, 11):
    # Create a DataFrame with the current message
    message = f"message {i}"
    data = [(message,),]
    df = spark.createDataFrame(data, ["value"])
    df.show()
    # Write the DataFrame to Kafka
    df.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("topic", "events_topic") \
        .save()


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
    .option("kafka.bootstrap.servers", "b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092,") \
    .option("subscribe", "retail_transactions") \
    .load()

# Deserialize the value from Kafka message
transactions = df.selectExpr("CAST(value AS STRING)").selectExpr("from_json(value, schema) as data").select("data.*")

transactions = (df.selectExpr("CAST(value AS STRING)")
                .withColumn("data", from_json(col("value"), schema))
                .select("data.*"))

