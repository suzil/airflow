# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import unittest
from airflow import DAG
from airflow import configuration
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.contrib.sensors.redis_key_sensor import RedisKeySensor
from airflow.utils import timezone

DEFAULT_DATE = timezone.datetime(2017, 1, 1)


class TestRedisSensor(unittest.TestCase):

    def setUp(self):
        configuration.load_test_config()
        args = {
            'owner': 'airflow',
            'start_date': DEFAULT_DATE
        }

        self.dag = DAG('test_dag_id', default_args=args)
        self.sensor = RedisKeySensor(
            task_id='test_task',
            redis_conn_id='redis_default',
            dag=self.dag,
            key='test_key'
        )

    def test_poke(self):
        hook = RedisHook(redis_conn_id='redis_default')
        redis = hook.get_conn()
        redis.set('test_key', 'test_value')
        self.assertTrue(self.sensor.poke(None), "Key exists on first call.")
        redis.delete('test_key')
        self.assertFalse(self.sensor.poke(None), "Key does NOT exists on second call.")


if __name__ == '__main__':
    unittest.main()
