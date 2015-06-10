import arrow
import evelink
from six import itervalues, iteritems

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def safe_redirect(endpoint='MetaView:index', next=None, **kwargs):
    if is_safe_url(next):
        return redirect(next)
    target = get_redirect_target()
    return redirect(target or url_for(endpoint, **kwargs))



def humanize(date):
    try:
        return arrow.get(date).humanize()
    except Exception:
        return 'Invalid date'


def format_datetime(date):
    try:
        return arrow.get(date).format('DD MMMM YYYY - HH:ss')
    except Exception:
        return 'Invalid date'


def get_alliance(id):
    eve = evelink.eve.EVE()
    alliances = eve.alliances()
    return next(alliance for alliance in itervalues(alliances[0]) if alliance['id'] == id)

def get_corporation(id):
    api = evelink.api.API()
    corp = evelink.corp.Corp(api)
    return corp.corporation_sheet(id)[0]

def get_standing(id):
    key = current_app.config.get('CONTACT_KEY', '').split(',')
    if key is None:
        current_app.logger.warning('No contact key set, returning standing 0. Please set a contact key.')
        return 0
    api = evelink.api.API(api_key=tuple(key))
    corp = evelink.corp.Corp(api)
    contacts = corp.contacts()
    if id in contacts[0]['alliance']:
        return contacts[0]['alliance'][id]['standing']
    elif id in contacts[0]['corp']:
        return contacts[0]['corp'][id]['standing']
    else:
        return 0
