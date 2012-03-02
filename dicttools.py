#!/usr/bin/python

#
# Functions for better dictionary usage
#

def union(dicta, dictb, join_fn):
    """Joins two dictionaries, (dicta and dictb) using join_fn to handle key collisions.
    The value of any pair of keys that collide is join_fn(v1, v2)"""
    result = dicta.copy()   
    for k,v in dictb.iteritems():
        if result.has_key(k):
            result[k] = join_fn(result[k], v)
        else:
            result[k] = v
    return result

def dunion(dicta, dictb, join_fn):
    """Destructively joins two dictionaries, (dicta and dictb) using 
    join_fn to handle key collisions.
    The value of any pair of keys that collide is join_fn(v1, v2).
    dicta is the destructively updated dictionary."""
    for k,v in dictb.iteritems():
        if dicta.has_key(k):
            dicta[k] = join_fn(dicta[k], v)
        else:
            dicta[k] = v
    return dicta 

def union_add(dicta, dictb):
    return union(dicta, dictb, lambda a, b: a + b)

def dunion_add(dicta, dictb):
    return dunion(dicta, dictb, lambda a, b: a + b)
