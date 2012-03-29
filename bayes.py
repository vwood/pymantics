#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naïve Bayesian Classifier
#

class Bayes():
    """Data should be a set of terms."""
    def __init__(self):
        self.total_count = 0
        
        # labels = {label: count}
        self.labels = {}
        
        # data = {labels: {data : count}}
        self.label_data = {}

        self.data = set()

    def train(self, data, label, count=1):
        if not self.labels.has_key(label):
            self.labels[label] = 0
        self.labels[label] += count
        
        self.total_count += count
        if not self.label_data.has_key(label):
            self.label_data[label] = {}
            
        this_label_data = self.label_data[label]
        for item in data:
            if not this_label_data.has_key(item):
                this_label_data[item] = 0
            this_label_data[item] += count
            self.data.add(item)

    def label_probability_absent_is_missing(self, data, label):
        """This version of label probability, ignores the absence of data values.
        (i.e. treats absent data values as unknown ones.)
        Use this if you're going to need missing data values *and* for every data value you have
        A and ~A as data values."""
        label_prob = self.labels[label] / float(self.total_count)
        prob = label_prob
        
        this_label_data = self.label_data[label]
        for item in data:
            extra_data_count = len(self.data) * len(self.labels)
            prob_label_and_item = ((this_label_data.get(item, 0) + 1) /
                                   float(self.total_count + extra_data_count))
            prob *= prob_label_and_item / label_prob

        return prob

    def label_probability_absent_is_negative(self, data, label):
        """This version of label probability treats absent data values as negative."""
        label_prob = self.labels[label] / float(self.total_count)
        prob = label_prob
        
        this_label_data = self.label_data[label]
        for item in self.data:
            # Total extra items (+1 for every category)
            extra_data_count = 2 * len(self.data) * len(self.labels)

            if item in data:
                prob_label_and_item = ((this_label_data.get(item, 0) + 1) /
                                       float(self.total_count + extra_data_count))
                prob *= prob_label_and_item / label_prob
            else:
                prob_label_and_item = ((self.labels[label] - this_label_data.get(item, 0) + 1) /
                                       float(self.total_count + extra_data_count))
                prob *= prob_label_and_item / label_prob
        return prob

    def label_probability(self, data, label, absent_is_missing=True):
        if absent_is_missing:
            return self.label_probability_absent_is_missing(data, label)
        else:
            return self.label_probability_absent_is_negative(data, label)
        
    def classify(self, data, absent_is_missing=True):
        max_prob = 0
        max_label = "default"
        for label in self.labels:
            label_prob = self.label_probability(data, label, absent_is_missing)
            if label_prob > max_prob:
                max_label = label
                max_prob = label_prob
            print label, label_prob
        return max_label, max_prob

if __name__ == '__main__':
    # Example using absent data values as missing (The default)
    # This implies each possible data value is part of an option type,
    # At most one option occuring
    b = Bayes()
    b.train(['a'], "x", 5)
    b.train(['~a'], "x", 10)
    b.train(['a'], "y", 10)
    b.train(['~a'], "y", 5)
    
    print b.classify(['a'], True)
    print b.classify(['~a'], True)

    # Example using absent data values as negative
    # This implies each possible data value is boolean (occurs or does not)
    b = Bayes()
    b.train(['a'], "x", 5)
    b.train([], "x", 10)
    b.train(['a'], "y", 10)
    b.train([], "y", 5)
    
    print b.classify(['a'], False)
    print b.classify([], False)
