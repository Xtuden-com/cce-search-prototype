from cce_search.api import search, reg_search, ren_search, registration, renewal
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import re
from urllib.parse import urlparse, parse_qs, parse_qsl, urlunparse, urlencode
from werkzeug.exceptions import abort
from requests import HTTPError

bp = Blueprint('search', __name__)

@bp.route('/')
def index():
    results = None
    title = None
    paging=None
    sentTitle = None
    search_type = "ft"
    arguments = request.args.get("title") or request.args.get("renewal") or request.args.get("registration") or request.args.get("author") or request.args.get("publisher")
    #print("TEST HERE")
    #print(request.args)
    #print(request.args.get("title"))
    print("----------------------------------------------------------")
    unique = 0
    
    if not arguments:
        print("NO ARGUMENTS GIVEN. PLEASE GIVE ARGUMENTS")
    else:
        if request.args.get("renewal"):
                results = ren_search(request.args['renewal'], request.args.get('page'),
                    request.args.get('per_page'))
                paging = proc_pagination(results['data']['paging'], request.args.get('page'))    
                unique = 1
        
        
        if request.args.get("registration") and unique == 0:
                results = reg_search(request.args['registration'], request.args.get('page'),
                    request.args.get('per_page'))
                paging = proc_pagination(results['data']['paging'], request.args.get('page'))
                unique = 1 #technically not 100% unique but should be very simplified for now
        
        if request.args.get("title") and unique == 0:
            title = request.args['title']
            results = search(title, request.args.get('page'),
                request.args.get('per_page'))
            paging = proc_pagination(results['data']['paging'],
                request.args.get('page'))
        
        
        if request.args.get("author") and unique == 0:
            results = search(request.args['author'], request.args.get('page'),
                    request.args.get('per_page'))
            paging = proc_pagination(results['data']['paging'],
                request.args.get('page'))
        
        
        if request.args.get("publisher") and unique == 0:
            results = search(request.args['publisher'], request.args.get('page'),
                    request.args.get('per_page'))
            paging = proc_pagination(results['data']['paging'],
                request.args.get('page'))
        #paging = proc_pagination(results['data']['paging'],
        #    request.args.get('page'))
        
        print("PRINTING PAGING HERE")
        print(paging) 
                           
        results = proc_results(results)
        print(results)
        
        if results == []:
            print("NO RESULTS")
            noresults = 1
            return render_template('search/index.html', noresults=noresults)
    
    return render_template('search/index.html', results=results, term=title,
            paging=paging, search_type=search_type)


def proc_results(r):
    return [enhance_results(res) for res in r['data']['results']]


def enhance_results(r):
    if r.get('type') == 'renewal':
        return r
    return {**r, **{'original': strip_tags(r.get('xml')),
                    'is_post_1963': is_post_1963(r.get('registrations')),
                    'is_foreign': is_foreign(r.get('registrations')),
                    'is_interim': is_interim(r.get('registrations')),
                    'source_url': ia_url(r.get('source', {}))}}


def strip_tags(xml):
    if xml:
        return re.sub(r"</?.+?>", "", xml).replace("\n", "")
    return ""


def ia_url(src): 
    #return src
    return "{}#page/{:d}/mode/1up".format(ia_stream(src.get('url', '')),
                                        src.get('page', 0))

def ia_stream(url):
    return url.replace('details', 'stream')


def is_post_1963(regs):
    return any([r['date'] > '1963' for r in regs])


def is_foreign(regs):
    return any([r['number'][:2] == 'AF' for r in regs])


def is_interim(regs):
    return any([r['number'][:2] == 'AI' for r in regs])


def proc_pagination(pg, current):
    if not pg['next'] and not pg['previous']:
        return {**pg, **{'has_pages': False}}

    per_page = extract_per_page(pg)

    if current is None:
        current = 1
    else:
        current = int(current) + 1
        
    
    return {**pg, **{'has_pages': True,
                     'current_page': current,
                     'last_page': extract_last(pg),
                     'pages': dict([(p, extract_pg(pg.get(p), per_page))
                               for p in ['first', 'next', 'last',
                                         'previous']])}}

def extract_pg(pg, per_page):
    if pg:
        oq = dict(parse_qsl(urlparse(pg).query))
        t = urlparse(request.url)
        return urlunparse(
            t._replace(query=urlencode({**dict(parse_qsl(t.query)),
                                        **{'page': oq['page'],
                                           'per_page': oq['per_page']}})))

    return None


def extract_per_page(pg):
    return [parse_qs(urlparse(v).query)["per_page"][0]
            for v in pg.values() if v][0]


def extract_last(pg):
    last = pg.get('last')
    if last is None:
        return "1"
    else:
        return int(parse_qs(urlparse(last).query)["page"][0]) + 1


@bp.route('/cceid/<cceid>')
def cceid(cceid):
    try:
        results = registration(cceid)
        return render_template('search/cceid.html', result=results["data"])
    except HTTPError:
        try:
            results = renewal(cceid)
            return render_template('search/cceid.html',
                                   result=results["data"][0])
        except HTTPError:
            pass

    return render_template('search/cceid.html', result=None, error=1)
    
        
