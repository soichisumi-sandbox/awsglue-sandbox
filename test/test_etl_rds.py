import pytest
import boto3
import json
import os
import sys
import io
import csv
from src.etl import load_dynamic_frame_from_csv
from botocore.client import Config
import MySQLdb
import random
import string

def randchar(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

def setup_rds():
    con = MySQLdb.connect(
        user='user',
        passwd='password',
        host='0.0.0.0',
        db='database',
        charset='utf8',
    )
    cur= con.cursor()
 
    # insert
    values = '';
    for i in range(10):
      if i != 0:
        values += ', '
      values += f'({randchar(10)}, {randchar(8)}.gmail.com)'

    sql = f"insert into `users` (`name`, `email`, `created`) VALUES {values};"
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

def test_load_dynamic_frame_from_csv():
    # setup
    setup_rds()
    sql 
    inputs = [
      {
        "id": "1",
        "name": "xxx",
        "address": "xxx@example.co.jp"
      },
      {
        "id": "2",
        "name": "yyy",
        "address": "yyy@example.co.jp"
      }
    ]
    input_str = io.StringIO()
    w = csv.DictWriter(input_str, fieldnames=inputs[0].keys())
    w.writeheader()
    for input in inputs:
      w.writerow(input)
    s3 = boto3.resource(
        "s3",
        endpoint_url=os.environ["TEST_S3_ENDPOINT_URL"],
        region_name="ap-northeast-1",
        use_ssl=False,
        config=Config(s3={"addressing_style": "path"}),
    )
    bucket_name = "test-csv-bucket"
    bucket = s3.Bucket(bucket_name)
    bucket.create(ACL="public-read-write")
    body = input_str.getvalue()
    key = "user/2019/12/06/users.csv"
    bucket.put_object(Key=key, Body=body, ACL="public-read-write")

    # exec
    res_df = load_dynamic_frame_from_csv(pytest.glueContext, pytest.spark, bucket_name, key)

    # assert
    assert res_df.count() == len(inputs)
    res_df_json = res_df.toDF().toJSON().take(len(inputs))
    for res in res_df_json:
      r = json.loads(res)
      assert r in inputs