# Mongodb Data Retriever
# Take in DB Credentials
# Return Dictionary -> Key: User, Value: (Date,Cost)
# California Plug Load Research Center, 2018
# Produced by Liangze Yu

import pymongo


class Data_Retriever:

    def __init__(self,host,port,db_name,collection_name):

        # set up connection
        self.__client = pymongo.MongoClient(host, port)
        self.__db = self.__client[f'{db_name}']
        self.__collection = self.__db[f'{collection_name}']

        # data filter
        self.__user = None
        self.__time = None
        self.__cost = None

        # return dictionary
        self.__user_time_cost = {}

    def set_retrieve_key(self,user,time,cost):
        self.__user = user
        self.__time = time
        self.__cost = cost

    def get_users(self):
        return self.__collection.distinct(self.__user)

    def get_data(self):
        '''
        :return: a dictionary, keys -> [users], values -> [(datetime,Kilowatts)]
        '''
        if self.__user == None or self.__time == None or self.__cost == None:
            print('WARNING, PLEASE SET UP FUNCTION "set_reterieve_key" FIRST.')
            exit(1)
        distinct_user = self.__collection.distinct(self.__user)
        for user in distinct_user:
            self.__user_time_cost[user] = []
            for document in self.__collection.find({'run':user}):
                self.__user_time_cost[user].append((document[self.__time],float(document[self.__cost])))
            #sort time, in case time data is not sorted by time
            self.__user_time_cost[user].sort()

        return self.__user_time_cost


if '__main__' == __name__:

    # Setup
    HOST = 'xxx'
    PORT = 0000
    DB = 'xxx'
    COLLECTION = 'xxx'
    USER_KEY = 'xxx'
    TIME_KEY = 'xxx'
    COST_KEY = 'xxx'

    #retriver object
    retriever = Data_Retriever(HOST,PORT,DB,COLLECTION)
    retriever.set_retrieve_key(USER_KEY,TIME_KEY,COST_KEY)
    print(retriever.get_data())



