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
        self.absent_is_missing = True

    def set_absent_is_missing(self, value):
        """"Should we treat absent values as missing values, or as Negative"""
        self.absent_is_missing = value

    def train(self, data, label, count=1):
        """Train the classifier on some data."""
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

    def label_probability(self, data, label):
        """Main dispatch for getting the probability of a label."""
        if self.absent_is_missing:
            return self.label_probability_absent_is_missing(data, label)
        else:
            return self.label_probability_absent_is_negative(data, label)
        
    def classify(self, data):
        max_prob = 0
        max_label = "default"
        evidence = 0
        for label in self.labels:
            label_prob = self.label_probability(data, label)
            evidence += label_prob
            if label_prob > max_prob:
                max_label = label
                max_prob = label_prob
        return max_label, max_prob, evidence

    def test(self, test_data):
        """Perform a test against some test data.
        Where the test_data is a [(data, label), ...]
        Returns a {label: (correct, incorrect)}."""
        result = {}
        for data, label in test_data:
            classified_as, _, _ = self.classify(data)
            correct, incorrect = result.get(label, (0,0))
            if classified_as == label:
                correct += 1
            else:
                incorrect += 1
            result[label] = (correct, incorrect)
        return result
    
if __name__ == '__main__':
    print "Example using absent data values as missing (The default):"
    print "This implies each possible data value is part of an option type,"
    print "at most one option occuring."
    b = Bayes()
    b.train(['a'], "x", 5)
    b.train(['~a'], "x", 10)
    b.train(['a'], "y", 10)
    b.train(['~a'], "y", 5)
    
    print b.classify(['a'])
    print b.classify(['~a'])

    print "Example using absent data values as negative:"
    print "This implies each possible data value is boolean (occurs or does not)"
    print "Results should be the same as the previous example."
    b = Bayes()
    b.set_absent_is_missing(False)
    b.train(['a'], "x", 5)
    b.train([], "x", 10)
    b.train(['a'], "y", 10)
    b.train([], "y", 5)
    
    print b.classify(['a'])
    print b.classify([])

    print "A more complex example, using test data:"
    b = Bayes()
    b.set_absent_is_missing(True)
    b.train(['a', 'b'], "x", 100)
    b.train(['~a', 'b'], "x", 90)
    b.train(['a', '~b'], "x", 50)
    b.train(['~a', '~b'], "x", 10)
    b.train(['a', 'b'], "y", 5)
    b.train(['~a', 'b'], "y", 10)
    b.train(['a', '~b'], "y", 30)
    b.train(['~a', '~b'], "y", 130)
    print b.classify(['a', 'b'])
    print b.classify(['a', '~b'])
    print b.classify(['~a', 'b'])
    print b.classify(['~a', '~b'])

    print b.test([(['a','b'], 'x'),
                  (['a','b'], 'x'),
                  (['~a','b'], 'x'),
                  (['~a','b'], 'x'),
                  (['a','b'], 'x'),
                  (['a','~b'], 'y'),
                  (['a','~b'], 'y'),
                  (['~a','~b'], 'y'),
                  (['~a','~b'], 'y')])

    
