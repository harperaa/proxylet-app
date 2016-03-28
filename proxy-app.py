# qiyan.zm@alibaba-inc.com
import proxylet, sys
from proxylet.relocate import Relocator, UrlInfo

routes = [
    ('http://localhost:7070/query-player', 'http://localhost:7070'),
    'http://localhost:5000'
]

def to_relocator(route):
    if type(route) == str: return None
    (local, remote) = route
    return Relocator(local, remote)

relocators = filter(lambda r: r, map(to_relocator, routes))

def mapper(req):
    for r in relocators: 
        if r.matchesLocal(req.reqURI):
            return r.mapping
    url = UrlInfo(routes[-1])
    return (url.host, url.port, None)

def main(port):
    try:
        proxylet.serve('', 7110, mapper)
    except (SystemExit, KeyboardInterrupt):
        print('bye')
        
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7110
    main(port)
