#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
import sys

import redis

reload(sys)
sys.setdefaultencoding("utf-8")


class Withdraw(object):
    def __init__(self):
        self.redis = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
            password=os.getenv("REDIS_PASSWORD"))

    def withdraw_now_playing_movies(self):
        sorted_movies = pickle.loads(self.redis.get('now_playing_movies'))
        return "\n".join("%s      %s" % tup for tup in sorted_movies)

    def withdraw_later_coming_movies(self):
        upcoming_movies = pickle.loads(self.redis.get("upcoming_movies"))
        return "\n".join("%s  %s 　%s 　%s" % (name, date, category, area)
                         for (name, date, category, area) in upcoming_movies)
