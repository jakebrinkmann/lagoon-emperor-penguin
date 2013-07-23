from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,get_list_or_404
from django.template import Context, loader, RequestContext
from ordering.models import Scene,Order,Configuration
from ordering.helper import *
import lta, re, json, core
from datetime import datetime


__author__ = "David V. Hill"
__api__version__ = "0.1.0"

def get_api_version():
    '''returns the current api version'''
    pass

def get_api_docs():
    '''returns the api documentation to the requestor'''
    pass

def _authenticate(request):
    '''Authenticates the incoming api request against LTA and returns assigned ESPA roles'''
    #call against LTA with user/password
    #if LTA returns valid creds, query ESPA db for roles
    #store the LTA id + roles in memcache temporarily with expiration time
    #return roles to caller or None if auth failure
    pass

def _validate_order_request(request):
    '''Checks the format of the incoming order request and ensures it is acceptable before proceeding'''
    #_validate_email(request['email'])
    #unmarshall from json and ensure it's valid
    #check for required fields and make sure they are there
    #check content of required fields
    pass

def _update_ordersize_limit_count(request, requested_unit_count):
    '''Captures the number of units ordered per user per day for use in rate limiting'''
    #update db with current daily requested unit count
    pass

def _is_order_under_daily_limit_count(request, requested_unit_count):
    '''Determines whether the incoming order can be placed and still keep the user under the daily
unit limit'''
    #check db for current count, add that size to requested size and see if it fits
    pass

def get_current_daily_limit_status(request, email):
    '''Returns the number of remaining units that can be submitted for the user for today'''
    #return rate limit minus submitted unit count for today
    pass

def get_example_place_order(request):
    '''Returns an example place_order json request'''
    pass

def get_example_order_status(request):
    '''Returns an example get_order_status request'''
    pass

@csrf_exempt       
def place_order(request):
    '''Accepts new order api requests'''
    #_authenticate(request)
    #_validate_order_request(request)
    #_is_order_under_daily_limit_status(request, len(request.get('scenes')))
    #_update_current_daily_limit_count(request, len(request.get('scenes')))
    #return 200 or 4xx status with error message                                     
    pass

@csrf_exempt        
def get_order_status(email, ordernum):
    '''Returns current status of requested order for user'''
    '''
    {
    'ordernum':'abc@def.com-1234567890',
    'status':'onorder',
    'date_submitted':'2013-07-15',
    'date_completed':'',
    'note':'',
    'selected_options':['sr', 'ndvi', 'ndmi', 'toa', 'source_metadata'],
    'units':[{
              'scenename':LE70290302003151EDC00,
              'status':'processing',
              'download_url':'',
              'cksum_download_url':'',
              'note':'',
              'date_completed', ''
             },

             {
              'scenename':LE70300302003151EDC00,
              'status':'queued',
              'download_url':'',
              'cksum_download_url':'',
              'note':'',
              'date_completed', ''
             },              
            ]
    }
    '''
    #return dict(order(email, ordernum))
    pass

def get_all_orders_status(email):
    '''Returns a full listing of all orders for the user'''
    '''
[
{
    'ordernum':'abc@def.com-1234567890',
    'status':'onorder',
    'date_submitted':'2013-07-15',
    'date_completed':'',
    'note':'',
    'selected_options':['sr', 'ndvi', 'ndmi', 'toa', 'source_metadata'],
    'units':[{
              'scenename':LE70290302003151EDC00,
              'status':'processing',
              'download_url':'',
              'cksum_download_url':'',
              'note':'',
              'date_completed', ''
             },

             {
              'scenename':LE70300302003151EDC00,
              'status':'queued',
              'download_url':'',
              'cksum_download_url':'',
              'note':'',
              'date_completed', ''
             },              
            ]
    }
],

    '''
    #return list(orders(email))
    pass

    
'''
REFERENCE ONLY, THIS WILL NOT BE PART OF THE API
@csrf_exempt
def get_order_details(request, orderid, output_format=None):
   
    #create placeholder for any validation errors
    errors = {}

    mimetype = None
    scenes = None
    #if we got here it's all good, display the orders
    if output_format is not None and output_format == 'csv':
        scenes = Scene.objects.filter(order__orderid=orderid,status='Complete')
        output = ''
        for scene in scenes:
            line = ("%s,%s,%s\n") % (scene.name,scene.download_url,scene.cksum_download_url)
            output = output + line
        return HttpResponse(output, mimetype='text/plain')
        
    else:
        order = Order.objects.get(orderid=orderid)
        scenes = Scene.objects.filter(order__orderid=orderid)
        t = loader.get_template('orderdetails.html')
        mimetype = 'text/html'   
        c = RequestContext(request)
        c['order'] = order
        c['scenes'] = scenes
        return HttpResponse(t.render(c), mimetype=mimetype)
        
'''     



        


