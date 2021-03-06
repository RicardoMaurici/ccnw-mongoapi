# encoding: iso-8859-1
import re
from flask import jsonify
from flask_pymongo import PyMongo

API_DATA_KEYS = (
    'title',
    'published_date',
    'scrapped_date',
    'domain',
    'url',
    'categories',
    'tags',
    'entities',
    'body',
    'risk'
)

API_DATA_KEYS_TYPE = (
    'string',
    'string',
    'string',
    'string',
    'string',
    'list of strings',
    'list of strings',
    'list of strings',
    'string',
    'string'
)

def serializer(raw):
    """
    Takes the raw input and return in the json format

    Parameters
    ----------
    raw : cursor object or dict

    Returns
    -------
    json
        json of the dicts

    """
    output = []
    if type(raw) is dict:
        output = removeID(raw)
    else:
        output = [removeID(x) for x in raw]
    return jsonify(output)


def removeID(raw_dict):
    """
    Takes the raw dict and return a without ones of its keys

    Parameters
    ----------
    raw_dict : dict

    Returns
    -------
    dict
        raw_dict without the id key
    """
    if '_id' in raw_dict:
        del raw_dict['_id']
    return raw_dict

def regexIt(raw_dict):
    """
    Takes the raw dict and return a formated in regular expresion

    Parameters
    ----------
    raw_dict : dict

    Returns
    -------
    dict
        formated dict with values as regular expressions
    """
    return {key : re.compile(value,re.IGNORECASE) for key, value in raw_dict.iteritems()}



KEYS_TYPE = zip(API_DATA_KEYS, API_DATA_KEYS_TYPE)

API_DOC = 'GET /news - To receive all the news on the database\n'\
'       Expected responses: 200\n\n'\
'GET /news?filter0=param&filterN=paramN - To receive all the news that pass on those filters\n'\
'       Allowed filters (name, type): {}'.format(KEYS_TYPE)+'\n'\
'       Expected responses: 200, 404\n\n'\
'POST /news - with payload in json format with the previous filters\n'\
'       Expected responses: 201, 400\n\n'\
'PATCH /news?filter0=param - with payload in json format with the some of the previous filters\n'\
'       Expected responses: 201, 204, 400\n\n'\
'OPTIONS /news - To get the api options\n'\
'       Expected responses: 200\n\n'\
'Example: Getting the news that has the category : "Corrupção"\n'\
'       GET /news?categories=Corrupção\n\n'\
'Example: Getting the news that has the category : "Corrupção" and are related to the person "João Silva"\n'\
'       GET /news?categories=Corrupção&people=João+Silva\n\n'\
'GET /keys - To receive all keys of each news on the database\n'\
'       Expected responses: 200\n\n'\
