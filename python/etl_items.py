import definitions
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType
import pandas as pd

def etl_items_spark():
    """
    ETL em PySpark do arquivo items.json.
    """
    try:
        spark = (
            SparkSession
            .builder
            .appName("etl_items")
            .getOrCreate()
        )
        # arquivo json de items
        json_file_path = definitions.ITEMS_JSON_PATH
        df_items = spark.read.json(json_file_path, multiLine=True)

        atributes = ['BRAND','COLOR','FIPE_PRICE','KILOMETERS','ENGINE','MODEL','VEHICLE_YEAR','TRANSMISSION']

        df_items_tratado = (
            df_items
            .select(
                F.col('id'),
                F.col('site_id'),
                F.col('title'),
                F.col('category_id'),
                F.coalesce(F.col('price'), F.lit(0)).cast(FloatType()).alias('price'),
                F.coalesce(F.col('base_price'), F.lit(0)).cast(FloatType()).alias('base_price'),
                F.coalesce(F.col('original_price'), F.lit(0)).cast(FloatType()).alias('original_price'),
                F.col('location.city.name').alias('city_name'),
                F.col('location.state.name').alias('state_name'),
                F.col('location.country.name').alias('country_name'),
                F.explode(F.col('attributes')).alias('attributes_exploded')
            )
            .withColumn('attribute_id', F.col('attributes_exploded.id'))
            .withColumn('attribute_name', F.col('attributes_exploded.name'))
            .withColumn('attribute_value', F.col('attributes_exploded.value_name'))
            .drop('attributes_exploded')
            .filter(F.col('attributes_exploded.id').isin(atributes))
        )

        df_items_pivoted = (
            df_items_tratado
            .withColumn('attribute_id', F.lower(F.col('attribute_id')))
            .groupBy(
                F.col('id'),
                F.col('site_id'),
                F.col('title'),
                F.col('category_id'),
                F.col('price'),
                F.col('base_price'),
                F.col('original_price'),
                F.col('city_name'),
                F.col('state_name'),
                F.col('country_name'),
            )
            .pivot('attribute_id')
            .agg(F.first('attribute_value'))
        )

        df_items_final = (
            df_items_pivoted
            .withColumn('fipe_price', F.regexp_replace('fipe_price', 'r\$', ''))
            .withColumn('fipe_price', F.regexp_replace('fipe_price', '\.', ''))
            .withColumn('fipe_price', F.regexp_replace('fipe_price', ',', '.'))
            .withColumn('fipe_price', F.trim('fipe_price').cast(FloatType()))
            .withColumn('fipe_price', F.coalesce('fipe_price', F.lit(0)))
            .withColumn('kilometers', F.trim(F.regexp_replace('kilometers', 'km', '')).cast(FloatType()))
            .withColumn('transmission_type', 
                        F.when(F.lower(F.col('transmission')).like('automátic%'), F.lit('Automática'))
                        .when(F.lower(F.col('transmission')).like('manual%'), F.lit('Manual'))
                        .otherwise(F.col('transmission'))
            )
        )

        df_items_final = df_items_final.toPandas()

        df_items_final.to_csv(
            definitions.ITEMS_CSV_PATH, 
            sep=';',
            header=True,
            encoding='UTF-8'
        )

        spark.stop()

    except Exception as e:
        print('ETL Error:', e)

if __name__ == '__main__':
    pass
