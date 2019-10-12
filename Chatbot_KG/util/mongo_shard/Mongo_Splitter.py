# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Mongo_Splitter.py
   Description :  Mongo数据库切分
   Author :       charl
   date：          2018/12/5
-------------------------------------------------
   Change Activity: 2018/12/5:
-------------------------------------------------
"""

import pymongo
import logging
import time

"""
    Chunk splitter that tries to balance the number of objects per chunk rather
    than their size.

    MongoDB balancer splits chunks based on the total size of each chunk.
    Sometimes this is not what you need and you would rather balance your chunks
    depending on the number of objects they contain, not their bytesize.

    This script goes through each shard of your cluster, counts the number
    of items in each chunk (which is quite expensive operation when you
    have a large number of chunks) and splits each chunk. It repeats this
    until all your chunks have less than a given number of objects in them.
    
    ==================================
    
    
"""

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)

class Shard():
    '''
    Represents a single shard of your cluster
    '''
    def __init__(self, database, collections, mongodata):
        self.database = database
        self.collections = collections
        self.name = mongodata['_id']
        self.host = mongodata['host']    # 这里拼接uri
        if '/' in self.host:
            # replicaset 这里的连接方式需要调试
            hosts = self.host.split('/')[1]
            self.connection = pymongo.MongoClient(host=hosts)
        self.count = {}
        self.chunks = {}

        # count the number of objects this shard has in each collection
        for collection in self.collections:
            self.count[collection] = self.connection[self.database][collection].count()
            self.chunks[collection] = []

    def refresh_chunk_count(self, collection):
        '''

        :param collection:
        :return:
        '''
        for chunk in self.chunks[collection]:
            shard_key = self.collections[collection]
            count = self.connection[self.database][collection].find({
                shard_key: {
                    "$gte": chunk['min'][shard_key],
                    "$lt": chunk['max'][shard_key],
                }
            }).count()
            chunk['count'] = count

class Cluster():
    def __init__(self, host, database, collections):
        self.connection = pymongo.MongoClient(host)
        self.database = database
        self.collection = collections
        self.update()

    def update(self):
        """
          Update info about the cluster - all shards and chunks it contains.
        """
        logging.info("Updating cluster info")
        self.shards = {}
        for shard in self.connection['config']['shards'].find():
            self.shards[shard['_id']] = Shard(self.database,
                                              self.collections,
                                              shard)

        for collection in self.collections:
            for chunk in self.connection['config']['chunks'].find(
                    {"ns": "{}.{}".format(self.database, collection)}):
                self.shards[chunk['shard']].chunks[collection].append(chunk)

    def get_locks(self):
        return [lock for lock in
                self.connection['config']['locks'].find({"state": 2})]

    def balancer_stopped(self):
        return self.connection['config']['settings'].find({
            "_id": "balancer"
        })[0]["stopped"]

    def stop_balancer(self):
        """ Stop the balancer and wait for locks to be released.
            Give up after 10 minutes """
        logging.info("Stopping balancer")
        self.connection['config']['settings'].update(
            {"_id": "balancer"}, {"$set": {"stopped": True}})
        if not self.balancer_stopped():
            raise Exception("Could not stop balancer")

        logging.info("Waiting for locks")
        retries = 0
        while len(self.get_locks()) and retries < 120:
            logging.info("Waiting for locks to be released: %s" % retries)
            time.sleep(5)
            retries += 1

        if len(self.get_locks()):
            self.start_balancer()
            raise Exception("Could not wait for locks, aborting")

    def start_balancer(self):
        logging.info("Starting balancer")
        retries = 0
        while self.balancer_stopped() and retries < 5:
            self.connection['config']['settings'].update(
                {"_id": "balancer"}, {"$set": {"stopped": False}})
        if self.balancer_stopped():
            raise Exception("Could not start balancer")

    def split_chunks(self, collection, max_count):
        logging.info("Starting recursive split")
        shard_key = self.collections[collection]
        need_to_split = True
        while need_to_split:
            need_to_split = False
            for shardname, shard in self.shards.iteritems():
                if len(shard.chunks[collection]):
                    perchunk = shard.count[collection] / len(shard.chunks[collection])
                else:
                    perchunk = 0
                logging.info("Shard {} has {} chunks in collection {},"
                             " {} objects, {} objects/chunk".format(
                    shard.name,
                    len(shard.chunks[collection]),
                    collection,
                    shard.count[collection],
                    perchunk
                ))
                shard.refresh_chunk_count(collection)
                for chunk in shard.chunks[collection]:
                    if chunk['count'] > max_count:
                        logging.info("- Chunk {} has {} objects,"
                                     " need to split...".format(
                            chunk['_id'], chunk['count']))
                        try:
                            split = self.connection['admin'].command(
                                'split',
                                '{}.{}'.format(self.database, collection),
                                find={shard_key: chunk['min'][shard_key]}
                            )
                            if 'ok' in split:
                                # If we succeed in splitting at least one chunk
                                # we set need_to_split to True again, forcing
                                # the whole process from scratch. A smarter
                                # way would be to keep recursively splitting a
                                # single chunk until it's broken down into
                                # smaller ones, but this works fine as well.
                                need_to_split = True
                                logging.info("Split OK")
                            else:
                                logging.error(split)
                        except pymongo.errors.OperationFailure as e:
                            # gotta keep splitting
                            logging.error(e)
            if need_to_split:
                self.update()


if __name__ == '__main__':
    logging.info("Starting")
    cluster = Cluster()