"""
Definition of views.
"""
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from app.models import *
from django.db import transaction


import urllib2
import json
import time

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    context={}
    context['Bus'] = 'Bus'
    context['Direction'] = 'Direction'
    context['Stopname'] = 'Stop'
    if request.user.is_authenticated():
        items = Item.objects.filter(user=request.user)
        return render(request,'app/index.html',{'items' : items})
    if not 'buslist' in request.GET and not 'direction' in request.GET:
        buslist = {
            '1 Freeport Road',
            '2  Mount Royal',
            '4  Troy Hill',
            '6  Spring Hill',
            '7  Spring Garden',
            '8  Perrysville',
            '11 Fineview',
            '12 McKnight',
            '13 Bellevue',
            '14 Ohio Valley',
            '15 Charles',
            '16 Brighton',
            '17 Shadeland',
            '18 Manchester',
            '20 Kennedy',
            '21 Coraopolis',
            '22 McCoy',
            '24 West Park',
            '26 Chartiers',
            '27 Fairywood',
            '29 Robinson',
            '31 Bridgeville',
            '36 Banksville',
            '38 Green Tree',
            '39 Brookline',
            '40 Mt. Washington',
            '41 Bower Hill',
            '43 Bailey',
            '44 Knoxville',
            '48 Arlington',
            '51 Carrick',
            '53 Homestead Park',
            '54 North Side - Oakland - South Side',
            '55 Glassport',
            '56 Lincoln Place',
            '57 Hazelwood',
            '58 Greenfield',
            '59 Mon Valley',
            '60 Walnut Crawford Village',
            '64 Lawrenceville - Waterfront',
            '65 Squirrel Hill',
            '67 Monroeville',
            '68 Braddock Hills',
            '69 Trafford',
            '71 Edgewood Town Center',
            '74 Homewood - Squirrel Hill',
            '75 Ellsworth',
            '77 Penn Hills',
            '78 Oakmont',
            '79 East Hills',
            '81 Oak Hill',
            '82 Lincoln',
            '83 Bedford Hill',
            '86 Liberty',
            '87 Friendship',
            '88 Penn',
            '89 Garfield Commons',
            '91 Butler Street',
            '93 Lawrenceville - Oakland - Hazelwood',
            '19L    Emsworth Limited',
            '28X    Airport Flyer',
            '51L    Carrick Limited',
            '52L    Homeville Limited',
            '53L    Homestead Park Limited',
            '61A    North Braddock',
            '61B    Braddock - Swissvale',
            '61C    McKeesport - Homestead'
            '61D    Murray',
            '71A    Negley',
            '71B    Highland Park',
            '71C    Point Breeze',
            '71D    Hamilton',
            'G2 West Busway - All Stops',
            'G3 Moon Flyer',
            'G31    Bridgeville Flyer',
            'O1 Ross Flyer',
            'O12    McKnight Flyer',
            'O5 Thompson Run Flyer',
            'P1 East Busway - All Stops',
            'P10    Allegheny Valley Flyer',
            'P12    Holiday Park Flyer',
            'P13    Mount Royal Flyer',
            'P16    Penn Hills Flyer',
            'P17    Lincoln Park Flyer',
            'P2 East Busway Short',
            'P3 East Busway - Oakland',
            'P67    Monroeville Flyer',
            'P68    Braddock Hills Flyer',
            'P69    Trafford Flyer',
            'P7 McKeesport Flyer',
            'P71    Swissvale Flyer',
            'P76    Lincoln Highway Flyer',
            'P78    Oakmont Flyer',
            'Y1 Large Flyer',
            'Y45    Baldwin Manor Flyer',
            'Y46    Elizabeth Flyer',
            'Y47    Curry Flyer',
            'Y49    Prospect Flyer'
        }
        context['buslist'] = buslist
        direction = {'INBOUND', 'OUTBOUND'} 
        context['direction'] = direction
        return render(request, 'app/index.html', context)
    
    return render(request, 'app/index.html', context)

def user_profile(request):
    busnum = request.POST['busnum']
    busnumonly = busnum.split(' ')[0]
    context={}
    direction = request.POST['direction']
    url = "http://realtime.portauthority.org/bustime/api/v2/getstops?key=AGqwpJtVsFgmULpgWHdH3vMdZ&format=json&rt=" + busnumonly + "&dir=" + direction  
    #r = requests.get(url)
    r = urllib2.urlopen(url).read()
    #data = r.json()
    data = json.loads(r)
    try:
        stopdata = data['bustime-response']['stops']
    except:
        context['Stopname'] = "No such stop"
        return redirect ('home')
    context['busnum'] = busnumonly
    context['direction'] = direction
    context['stopdata'] = stopdata
    context['Bus'] = busnum
    context['Direction'] = direction

    return render(request, 'app/index.html', context)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

@login_required(login_url='/login')
def favorites(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    items = Item.objects.filter(user=request.user)
    return render(request, 'app/favorites.html', {'items' : items})

@login_required(login_url='/login')
def retrieve_favorite(request, id):
    # Sets up list of just the logged-in user's (request.user's) items
    items = Item.objects.filter(id=id)
    url = items.url
    r = requests.get(url)
    data = r.json()
    stopdata = data['bustime-response']['stops']
    context = {'stopdata' : stopdata} 
    return render(request, 'app/favorites.html', context)

def retrieve(request):
    busnum = request.POST['Bus']
    busnumonly = busnum.split(' ')[0]
    context={}
    direction = request.POST['Direction']
    url = "http://realtime.portauthority.org/bustime/api/v2/getstops?key=AGqwpJtVsFgmULpgWHdH3vMdZ&format=json&rt=" + busnumonly + "&dir=" + direction  
    r = urllib2.urlopen(url).read()
    data = json.loads(r)
    stopdata = data['bustime-response']['stops']
    stopname = request.POST['stopname']
    stid = 0
    for stop in stopdata:
        if stop['stpnm'] == stopname:
            stid = stop['stpid']
    url = "http://realtime.portauthority.org/bustime/api/v2/getpredictions?key=AGqwpJtVsFgmULpgWHdH3vMdZ&format=json&stpid=" + stid
    r = urllib2.urlopen(url).read()
    data = json.loads(r)
    context['Bus'] = busnum
    context['Direction'] = direction
    context['Stopname'] = stopname

    try:
        print data
        realtimedata = data['bustime-response']['prd']
        for entry in realtimedata:
            print entry
            time_yo= entry['prdtm']
            print time_yo
            time_entr = time_yo.split(' ')[1]
            print time_entr
            dt = time.strptime(time_entr, "%H:%M")
            dt_now = datetime.now().timetuple()

            entry['prdtm'] = ((((dt.tm_min*60) + (dt.tm_hour*3600)) - ((dt_now.tm_min*60) + (dt_now.tm_hour*3600))) / 60) + 300
        context['realtimedata'] = realtimedata 
    except Exception as e:
        print "Exception"
        print str(e)
        return redirect('home') 
    
    buslist = {
            '1 Freeport Road',
            '2  Mount Royal',
            '4  Troy Hill',
            '6  Spring Hill',
            '7  Spring Garden',
            '8  Perrysville',
            '11 Fineview',
            '12 McKnight',
            '13 Bellevue',
            '14 Ohio Valley',
            '15 Charles',
            '16 Brighton',
            '17 Shadeland',
            '18 Manchester',
            '20 Kennedy',
            '21 Coraopolis',
            '22 McCoy',
            '24 West Park',
            '26 Chartiers',
            '27 Fairywood',
            '29 Robinson',
            '31 Bridgeville',
            '36 Banksville',
            '38 Green Tree',
            '39 Brookline',
            '40 Mt. Washington',
            '41 Bower Hill',
            '43 Bailey',
            '44 Knoxville',
            '48 Arlington',
            '51 Carrick',
            '53 Homestead Park',
            '54 North Side - Oakland - South Side',
            '55 Glassport',
            '56 Lincoln Place',
            '57 Hazelwood',
            '58 Greenfield',
            '59 Mon Valley',
            '60 Walnut Crawford Village',
            '64 Lawrenceville - Waterfront',
            '65 Squirrel Hill',
            '67 Monroeville',
            '68 Braddock Hills',
            '69 Trafford',
            '71 Edgewood Town Center',
            '74 Homewood - Squirrel Hill',
            '75 Ellsworth',
            '77 Penn Hills',
            '78 Oakmont',
            '79 East Hills',
            '81 Oak Hill',
            '82 Lincoln',
            '83 Bedford Hill',
            '86 Liberty',
            '87 Friendship',
            '88 Penn',
            '89 Garfield Commons',
            '91 Butler Street',
            '93 Lawrenceville - Oakland - Hazelwood',
            '19L    Emsworth Limited',
            '28X    Airport Flyer',
            '51L    Carrick Limited',
            '52L    Homeville Limited',
            '53L    Homestead Park Limited',
            '61A    North Braddock',
            '61B    Braddock - Swissvale',
            '61C    McKeesport - Homestead'
            '61D    Murray',
            '71A    Negley',
            '71B    Highland Park',
            '71C    Point Breeze',
            '71D    Hamilton',
            'G2 West Busway - All Stops',
            'G3 Moon Flyer',
            'G31    Bridgeville Flyer',
            'O1 Ross Flyer',
            'O12    McKnight Flyer',
            'O5 Thompson Run Flyer',
            'P1 East Busway - All Stops',
            'P10    Allegheny Valley Flyer',
            'P12    Holiday Park Flyer',
            'P13    Mount Royal Flyer',
            'P16    Penn Hills Flyer',
            'P17    Lincoln Park Flyer',
            'P2 East Busway Short',
            'P3 East Busway - Oakland',
            'P67    Monroeville Flyer',
            'P68    Braddock Hills Flyer',
            'P69    Trafford Flyer',
            'P7 McKeesport Flyer',
            'P71    Swissvale Flyer',
            'P76    Lincoln Highway Flyer',
            'P78    Oakmont Flyer',
            'Y1 Large Flyer',
            'Y45    Baldwin Manor Flyer',
            'Y46    Elizabeth Flyer',
            'Y47    Curry Flyer',
            'Y49    Prospect Flyer'
        }
    context['buslist'] = buslist
    direction = {'INBOUND', 'OUTBOUND'} 
    context['direction'] = direction
    
    return render(request, 'app/index.html', context)     

@login_required(login_url='/login')
@transaction.atomic
def add_favorite(request):
    # errors = []

    # # Creates a new item if it is present as a parameter in the request
    # if not 'item' in request.POST or not request.POST['item']:
    #   errors.append('You havent selected anything to add.')
    # else:
    name = request.GET['name']
    stid = request.GET['stid']
    url = "http://realtime.portauthority.org/bustime/api/v2/getpredictions?key=AGqwpJtVsFgmULpgWHdH3vMdZ&format=json&stpid=" + stid 
    new_item = Item(name=name, url=url, user=request.user)
    new_item.save()
    return render(request, 'app/favorites.html', context)
    

@login_required(login_url='/login')
@transaction.atomic
def delete_favorite(request, id):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
        item_to_delete = Item.objects.get(id=id, user=request.user)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The item did not exist in your todo list.')

    context = {'errors' : errors}
    return render(request, 'app/favorites.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'app/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'app/register.html', context)

    print request.POST['password']
    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password'])
    new_user.save()

    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password'])

    login(request,new_user)

    return redirect('/favorites')

