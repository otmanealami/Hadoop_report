#!/usr/bin/env python
# coding: utf-8

from mrjob.job import MRJob 
from mrjob.step import MRStep 
from mrjob.protocol import JSONValueProtocol
import re
import string
"""
in this code , we will be extracting the 
payment method with highest amount by city in our file purchases.txt
the file is presented as follows : 
date hour city category amount paymentmethod
"""
class MRCITYPAYMENT(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol 
    """
    let's define our schema steps for the job
    two mapper a,d reducer are uses"""
    def steps(self): 
        return [ 
            MRStep(mapper=self.map_cities, reducer=self.profit_by_city_by_method), 
            MRStep(mapper=self.remap_function, reducer=self.best_purchased_methods) 
            ]

    def map_cities(self, __, line):
        """map function for cleaning entries by removing space and dividing lines using '\t' delimiter"""
        line = line.strip()
        t = line.split('\t')
        #if len(t)!=6: 
        yield (t[2].lower(), t[5].lower()), float(t[4])
        # a output of  (city ,paymentmethod ) by amount is generated

    def profit_by_city_by_method(self, method_city, values): 
        """this function reduces the mapping done to have the most profit got for the payment method"""
        profit_sum = 0 
        for profit in values: 
            profit_sum += profit
        
        yield method_city, profit_sum

    def remap_function(self, city_category, values): 
        """function to remap the ouput in the chema of city, (method, profit)"""
        city, method = city_category 
        yield city, (method, values)

    def best_purchased_methods(self, city, values): 
        ## function to reduce the previous mapping into the desired output 
        ##  top method is regenrated along with the top profit correspanding 
        ## to the highest profit observed by payment method bu city
        top_profit = 0
        top_method = ''
        for method, profit in values: 
            if profit > top_profit:
                top_profit = profit
                top_method = method
            
        yield None, (city, top_method,round(top_profit))

## running the built class
if __name__ == '__main__':
     MRCITYPAYMENT.run()