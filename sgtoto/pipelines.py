# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem
# Deprecated
#from scrapy import log

class CheckLatestDraw(object):
    #Initialise the database
    def __init__(self):
        logger = logging.getLogger()
        try:
            connection = pymongo.MongoClient(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']
            )
            logger.info("Connection to MongoDB Successful")
        except:
            logger.info("Connection to MongoDB Unsuccessful")
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        logger = logging.getLogger()
        valid = True
        logger.info("Getting Last Stored Draw from MongoDB")
        draw_cur = self.collection.find().sort([("latestdraw", pymongo.DESCENDING)]).limit(1)
        for doc in draw_cur:
            logger.info("Result of Last Stored Draw: %s", doc)
            latest_stored_draw = doc['latestdraw']
        logger.info("The latest draw from mongoDB: %s" % latest_stored_draw)
        for data in item:
            if not data:
                valid = False
                raise DropItem("Mission {0}".format(data))
        if valid:
            scraped_draw = item['latestdraw']
            if scraped_draw == latest_stored_draw:
                raise DropItem("Data is the latest")
                logger.info("Data is the Latest")
                return ("Data is the latest")
            else:
                self.collection.insert(dict(item))
                logger.info("Latest SGToto Draw added to MongDB Collection!")
        return item
