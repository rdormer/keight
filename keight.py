# -*- coding: utf-8 -*-

__all__ = (
    'PY2', 'PY3', 'U', 'B', 'S',
    'on', 'mapping',
    'ActionMapping', 'ActionEagerMapping', 'ActionLazyMapping',
    'BaseAction', 'Action', 'Request', 'Response',
    'WSGIApplication',
    'HttpException',
)

import sys, os, re, json, traceback
try:
    import re2
    def re_compile(pattern):
        return re2._compile(pattern)
except ImportError:
    def re_compile(pattern):
        return re._compile(pattern, 0)

def re_compile(pattern):
    return re._compile(pattern, 0)


setup_testing_defaults = None  # import from wsgi.util
BytesIO = None   # io.BytesIO or cStringIO.StringIO

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
assert PY2 or PY3, "Unexpected python version (%s)" % (sys.version)

if PY3:
    unicode     = str
    xrange      = range
    basestring  = str


ENCODING='utf-8'

def U(v, encoding=None):
    if isinstance(v, unicode):
        return v
    if isinstance(v, bytes):
        return v.decode(encoding or ENCODING)
    raise TypeError("%r: unicode expected.")

def B(v, encoding=None):
    if isinstance(v, bytes):
        return v
    if isinstance(v, unicode):
        return v.encode(encoding or ENCODING)
    raise TypeError("%r: bytes expected.")

if PY2:
    S = B
elif PY3:
    S = U


HTTP_STATUS_DICT = {
    100: "100 Continue",
    101: "101 Switching Protocols",
    102: "102 Processing",                # (WebDAV; RFC 2518)
    #
    200: "200 OK",
    201: "201 Created",
    202: "202 Accepted",
    203: "203 Non-Authoritative Information",  # (since HTTP/1.1)
    204: "204 No Content",
    205: "205 Reset Content",
    206: "206 Partial Content",           # (RFC 7233),
    207: "207 Multi-Status",              # (WebDAV; RFC 4918)
    208: "208 Already Reported",          # (WebDAV; RFC 5842)
    226: "226 IM Used",                   # (RFC 3229)
    #
    300: "300 Multiple Choices",
    301: "301 Moved Permanently",
    302: "302 Found",
    303: "303 See Other",                 # (since HTTP/1.1)
    304: "304 Not Modified",              # (RFC 7232)
    305: "305 Use Proxy",                 # (since HTTP/1.1)
    306: "306 Switch Proxy",
    307: "307 Temporary Redirect",        # (since HTTP/1.1)
    308: "308 Permanent Redirect",        # (RFC 7538)
   #308: "308 Resume Incomplete",         # (Google)
    #
    400: "400 Bad Request",
    401: "401 Unauthorized",              # (RFC 7235)
    402: "402 Payment Required",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    406: "406 Not Acceptable",
    407: "407 Proxy Authentication Required", # (RFC 7235)
    408: "408 Request Timeout",
    409: "409 Conflict",
    410: "410 Gone",
    411: "411 Length Required",
    412: "412 Precondition Failed",       # (RFC 7232)
    413: "413 Payload Too Large",         # (RFC 7231)
    414: "414 Request-URI Too Long",
    415: "415 Unsupported Media Type",
    416: "416 Requested Range Not Satisfiable",  # (RFC 7233)
    417: "417 Expectation Failed",
    418: "418 I'm a teapot",              # (RFC 2324)
    419: "419 Authentication Timeout",    # (not in RFC 2616)
    420: "420 Method Failure",            # (Spring Framework)
    420: "420 Enhance Your Calm",         # (Twitter)
    421: "421 Misdirected Request",       # (RFC 7540)
    422: "422 Unprocessable Entity",      # (WebDAV; RFC 4918)
    423: "423 Locked",                    # (WebDAV; RFC 4918)
    424: "424 Failed Dependency",         # (WebDAV; RFC 4918)
    426: "426 Upgrade Required",
    428: "428 Precondition Required",     # (RFC 6585)
    429: "429 Too Many Requests",         # (RFC 6585)
    431: "431 Request Header Fields Too Large", # (RFC 6585)
    440: "440 Login Timeout",             # (Microsoft)
    444: "444 No Response",               # (Nginx)
    449: "449 Retry With",                # (Microsoft)
    450: "450 Blocked by Windows Parental Controls", # (Microsoft)
    451: "451 Unavailable For Legal Reasons", # (Internet draft)
    451: "451 Redirect",                  # (Microsoft)
    494: "494 Request Header Too Large",  # (Nginx)
    495: "495 Cert Error",                # (Nginx)
    496: "496 No Cert",                   # (Nginx)
    497: "497 HTTP to HTTPS",             # (Nginx)
    498: "498 Token expired/invalid",     # (Esri)
    499: "499 Client Closed Request",     # (Nginx)
   #499: "499 Token required",            # (Esri)
    #
    500: "500 Internal Server Error",
    501: "501 Not Implemented",
    502: "502 Bad Gateway",
    503: "503 Service Unavailable",
    504: "504 Gateway Timeout",
    505: "505 HTTP Version Not Supported",
    506: "506 Variant Also Negotiates",   # (RFC 2295)
    507: "507 Insufficient Storage",      # (WebDAV; RFC 4918)
    508: "508 Loop Detected",             # (WebDAV; RFC 5842)
    509: "509 Bandwidth Limit Exceeded",  # (Apache bw/limited extension)
    510: "510 Not Extended",              # (RFC 2774)
    511: "511 Network Authentication Required", # (RFC 6585)
    520: "520 Unknown Error",
}

MIME_TYPES = {
    '.html'    : "text/html",
    '.htm'     : "text/html",
    '.shtml'   : "text/html",
    '.css'     : "text/css",
    '.csv'     : "text/comma-separated-values",
    '.tsv'     : "text/tab-separated-values",
    '.xml'     : "text/xml",
    '.mml'     : "text/mathml",
    '.txt'     : "text/plain",
    '.wml'     : "text/vnd.wap.wml",
    '.gif'     : "image/gif",
    '.jpeg'    : "image/jpeg",
    '.jpg'     : "image/jpeg",
    '.png'     : "image/png",
    '.tif'     : "image/tiff",
    '.tiff'    : "image/tiff",
    '.ico'     : "image/x-icon",
    '.bmp'     : "image/x-ms-bmp",
    '.svg'     : "image/svg+xml",
    '.svgz'    : "image/svg+xml",
    '.webp'    : "image/webp",
    '.mid'     : "audio/midi",
    '.midi'    : "audio/midi",
    '.kar'     : "audio/midi",
    '.mp3'     : "audio/mpeg",
    '.ogg'     : "audio/ogg",
    '.m4a'     : "audio/x-m4a",
    '.ra'      : "audio/x-realaudio",
    '.3gpp'    : "video/3gpp",
    '.3gp'     : "video/3gpp",
    '.3g2'     : "video/3gpp2",
    '.ts'      : "video/mp2t",
    '.mp4'     : "video/mp4",
    '.mpeg'    : "video/mpeg",
    '.mpg'     : "video/mpeg",
    '.mov'     : "video/quicktime",
    '.webm'    : "video/webm",
    '.flv'     : "video/x-flv",
    '.m4v'     : "video/x-m4v",
    '.mng'     : "video/x-mng",
    '.asx'     : "video/x-ms-asf",
    '.asf'     : "video/x-ms-asf",
    '.wmv'     : "video/x-ms-wmv",
    '.avi'     : "video/x-msvideo",
    '.json'    : "application/json",
    '.js'      : "application/javascript",
    '.atom'    : "application/atom+xml",
    '.rss'     : "application/rss+xml",
    '.doc'     : "application/msword",
    '.pdf'     : "application/pdf",
    '.ps'      : "application/postscript",
    '.eps'     : "application/postscript",
    '.ai'      : "application/postscript",
    '.rtf'     : "application/rtf",
    '.xls'     : "application/vnd.ms-excel",
    '.eot'     : "application/vnd.ms-fontobject",
    '.ppt'     : "application/vnd.ms-powerpoint",
    '.key'     : "application/vnd.apple.keynote",
    '.pages'   : "application/vnd.apple.pages",
    '.numbers' : "application/vnd.apple.numbers",
    '.zip'     : "application/zip",
    '.lha'     : "application/x-lzh",
    '.lzh'     : "application/x-lzh",
    '.tar'     : "application/x-tar",
    '.tgz'     : "application/x-tar",
    '.gz'      : "application/x-gzip",
    '.bz2'     : "application/x-bzip2",
    '.xz'      : "application/x-xz",
    '.7z'      : "application/x-7z-compressed",
    '.rar'     : "application/x-rar-compressed",
    '.rpm'     : "application/x-redhat-package-manager",
    '.deb'     : "application/vnd.debian.binary-package",
    '.swf'     : "application/x-shockwave-flash",
    '.der'     : "application/x-x509-ca-cert",
    '.pem'     : "application/x-x509-ca-cert",
    '.crt'     : "application/x-x509-ca-cert",
    '.xpi'     : "application/x-xpinstall",
    '.xhtml'   : "application/xhtml+xml",
    '.xspf'    : "application/xspf+xml",
    '.yaml'    : "application/x-yaml",
    '.yml'     : "application/x-yaml",
    '.docx'    : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    '.xlsx'    : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    '.pptx'    : "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def dict2json(jdict):
    return json.dumps(jdict, ensure_ascii=False, indent=None,
                      separators=_dict2json_seps, encoding=ENCODING)
_dict2json_seps = (',', ':')

#try:
#    re_compile = re._compile    # not cache
#except AttributeError:
#    re_compile = re.compile     # with cache

def re_escape(text):
    return re.sub(r'([-+\\.*?{}()&^$|\[\]])', r'\\\1', text)


def load_module(string):
    mod = __import__(string)
    for x in string.split('.')[1:]:
        mod = getattr(mod, x)
    return mod


def load_class(string):
    idx = string.rfind('.')
    if idx < 0:
        module_path = None
        class_name  = string
    else:
        module_path = string[:idx]
        class_name  = string[idx+1:]
    mod = load_module(module_path)
    return getattr(mod, class_name)


class HttpException(Exception):

    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers


class BaseAction(object):

    def __init__(self, req, resp):
        self.req  = req
        self.resp = resp

    def before_action(self):
        pass

    def after_action(self, ex):
        pass

    def run_action(self, action_func, action_args):
        self.action_func = action_func
        #
        ex = None
        try:
            self.before_action()
            content = self.handle_action(action_func, action_args)
            return self.handle_content(content)
        except Exception as ex_:
            ex = ex_
            raise
        finally:
            self.after_action(ex)

    def handle_action(self, action_func, action_args):
        if isinstance(action_args, dict):
            return action_func(self, **action_args)
        else:
            return action_func(self, *action_args)

    def handle_content(self, content):
        return content


class Action(BaseAction):

    default_content_type = "text/html;charset=utf-8"
    json_content_type    = "application/json"

    def dict2json(self, jdict):
        return dict2json(jdict)

    def handle_content(self, content):
        if content is None:
            binary = b""
        elif isinstance(content, dict):
            binary = self.dict2json(content)
            if isinstance(binary, unicode):
                binary = binary.encode('utf-8')   # JSON should be utf-8
            #self.resp.content_type = self.json_content_type
            self.resp.header_list[0] = ('Content-Type', self.json_content_type)
        elif isinstance(content, unicode):
            binary = content.encode(ENCODING)
        elif isinstance(content, bytes):
            binary = content
        else:
            return content   # TODO
        #
        #self.resp.content_length = len(binary)
        self.resp.header_list[1] = ('Content-Length', str(len(binary)))
        return [binary]

    def after_action(self, ex):
        #if not self.resp.content_type:    # slow
        #    self.resp.content_type = self.guess_content_type() or self.default_content_type
        if not self.resp.header_list[0][1]:
            self.resp.header_list[0] = ('Content-Type', self.guess_content_type() or self.default_content_type)

    def guess_content_type(self):
        #ext = os.path.splitext(self.req.path)[0]   # slow
        #return MIME_TYPES.get(ext)
        req_path = self.req.path
        pos = req_path.rfind('.')
        if pos < 0:
            return None
        return MIME_TYPES.get(req_path[pos:])


class ActionMethodMapping(object):

    def __init__(self):
        self._list = []

    def add(self, urlpath_pat, request_method, action_func):
        available_methods = ActionMapping.REQUEST_METHODS
        if request_method not in available_methods:
            raise ValueError("%s: Unknown request method." % (request_method,))
        dictionary = self._find_or_create(urlpath_pat)
        dictionary[request_method] = action_func
        return self

    def _find_or_create(self, urlpath_pat):
        for upath, dct in self._list:
            if upath == urlpath_pat:
                return dct
        dct = {}
        self._list.append((urlpath_pat, dct))
        return dct

    def __iter__(self):
        return self._list.__iter__()


def _get_mapping_obj(depth=2):
    localvars = sys._getframe(depth).f_locals
    key = '__mapping__'
    if key not in localvars:
        localvars[key] = ActionMethodMapping()
    return localvars[key]


def mapping(urlpath_pat, **kwargs):
    mapping_obj = _get_mapping_obj(2)
    for meth, func in kwargs:
        mapping_obj.add(urlpaht_pat, meth, func)
    return mapping_obj


def on(request_method, urlpath_pattern, **tags):
    mapping_obj = _get_mapping_obj(2)
    def deco(func):
        func.tags = tags
        mapping_obj.add(urlpath_pattern, request_method, func)
        return func
    return deco


class ActionMapping(object):

    REQUEST_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH',
                       'HEAD', 'OPTIONS', 'TRACE', 'LINK', 'UNLINK', ]

    URLPATH_PARAMETER_REXP = re.compile(r'\{(\w*)(?::(.*?))?\}')  # not re_compile()!

    def lookup(req_urlpath):
        raise NotImplementedError("%s.lookup(): not implemented yet." % self.__class__.__name__)

    def _upath_pat2rexp(self, pat, begin='', end='', capture=True):
        buf = [begin]
        pos = 0
        for m in self.URLPATH_PARAMETER_REXP.finditer(pat):
            text = pat[pos:m.start(0)]
            pname = m.group(1)    # urlpath parameter name
            rexp_str = m.group(2) or '[^/]+'
            pos = m.end(0)
            if capture and pname:
                buf.extend((re_escape(text), '(?P<%s>' % pname, rexp_str, ')', ))
            else:
                buf.extend((re_escape(text), '(?:',             rexp_str, ')', ))
        buf.extend((re_escape(pat[pos:]), end))
        return "".join(buf)

    def _load_action_class(self, class_string):  # ex: 'my.api.HelloAction'
        action_class = load_class(class_string)
        if not action_class:
            raise ValueError("%s: No such module or class." % class_string)
        self._validate_action_class(action_class)
        return action_class

    def _validate_action_class(self, action_class):
        if not isinstance(action_class, type):
            raise TypeError("%r: Action class expected." % (action_class,))
        if not issubclass(action_class, Action):
            raise TypeError("%s: Action class expected." % action_class.__name__)
        if not hasattr(action_class, '__mapping__'):
            raise ValueError("%s: No action methods." % action_class.__name__)


class ActionEagerMapping(ActionMapping):

    def __init__(self, mappings):
        self._fixed_urlpaths    = {}
        self._variable_urlpaths = []
        self._all_urlpaths      = []
        rexp_buf = self._build(mappings, "", ['^'])
        rexp_buf.append('$')
        self._variable_rexp = re_compile(''.join(rexp_buf))

    def _build(self, mappings, base_upath_pat, rexp_buf):
        rexp_buf.append('(?:')
        length = len(rexp_buf)
        #
        for upath_pat, item in mappings:
            rexp_str = self._upath_pat2rexp(upath_pat, '', '', False)
            rexp_buf.append(rexp_str)
            n = len(rexp_buf)
            #
            full_upath_pat = base_upath_pat + upath_pat
            if isinstance(item, list):
                rexp_buf.append(base_upath_pat)
                self._build(item, full_upath_pat, rexp_buf)
            else:
                if isinstance(item, basestring):
                    action_class = self._load_action_class(item)
                else:
                    action_class = item
                    self._validate_action_class(action_class)
                self._register(action_class, full_upath_pat, rexp_buf)
            #
            if len(rexp_buf) == n:
                rexp_buf.pop()
            else:
                rexp_buf.append('|')
        #
        if rexp_buf[-1] == '|':
            rexp_buf.pop()
        if len(rexp_buf) == length:
            rexp_buf.pop()
        else:
            rexp_buf.append(')')
        return rexp_buf

    def _register(self, action_class, base_upath_pat, rexp_buf):
        action_method_mapping = getattr(action_class, '__mapping__')
        if action_method_mapping is None:
            raise ValueError("%s: There is no action method mapping." % action_class.__name__)
        rexp_strs = []
        for upath_pat, action_methods in action_method_mapping:
            full_upath_pat = base_upath_pat + upath_pat
            if '{' in full_upath_pat:
                #rexp_str = self._upath_pat2rexp(full_upath_pat, '^', '$')
                #upath_rexp = re_compile(rexp_str)
                #
                arr = self.URLPATH_PARAMETER_REXP.split(full_upath_pat)
                if len(arr) == 2:
                    pname = self.URLPATH_PARAMETER_REXP.search(full_upath_pat).group(1)
                    upath_rexp = (pname, len(arr[0]), -len(arr[1]))  # instead of rexp
                else:
                    rexp_str = self._upath_pat2rexp(full_upath_pat, '^', '$')
                    upath_rexp = re_compile(rexp_str)
                #
                tupl = (action_class, action_methods, upath_rexp)
                self._variable_urlpaths.append(tupl)
                rexp_strs.append(self._upath_pat2rexp(upath_pat, '', r'($)', False))
            else:
                tupl = (action_class, action_methods)
                self._fixed_urlpaths[full_upath_pat] = tupl
            self._all_urlpaths.append((full_upath_pat, action_class, action_methods))
        if rexp_strs:
            if len(rexp_strs) == 1:
                rexp_buf.append(rexp_strs[0])
            else:
                rexp_buf.extend(('(?:', '|'.join(rexp_strs), ')'))

    def lookup(self, req_urlpath):
        tupl = self._fixed_urlpaths.get(req_urlpath)
        if tupl:
            action_class, action_methods = tupl
            pargs = {}
            return action_class, action_methods, pargs
        #for tupl in self._variable_urlpaths:
        #    action_class, action_methods, upath_rexp = tupl
        #    m = upath_rexp.match(req_urlpath)
        #    if m:
        #        pargs = m.groupdict()
        #        return action_class, action_methods, pargs
        #return None
        m = self._variable_rexp.match(req_urlpath)
        if m is None:
            return None
        idx = m.groups().index('')
        action_class, action_methods, upath_rexp = self._variable_urlpaths[idx]
        if isinstance(upath_rexp, tuple):
            pname, start, end = upath_rexp
            pval = req_urlpath[start:end] if end else req_urlpath[start:]
            pargs = {pname: pval} if pname else {}
        else:
            m = upath_rexp.match(req_urlpath)
            pargs = m.groupdict()
        return action_class, action_methods, pargs

    def __iter__(self):
        for tupl in self._all_urlpaths:
            urlpath_pat, action_class, action_methods, _, _ = tupl
            yield urlpath_pat, action_class, action_methods


class ActionEagerMapping2(ActionMapping):

    def __init__(self, mappings):
        self._all_urlpaths = []
        self._fixed_urlpaths = {}
        self._variable_urlpath_tuples = self._build(mappings, '', False)

    def _build(self, mappings, base_upath_pat, has_params):
        tuples = []
        for upath_pat, item in mappings:
            urlpath_pat = base_upath_pat + upath_pat
            has_params2 = has_params or '{' in upath_pat
            if isinstance(item, list):
                children = self._build(item, urlpath_pat, has_params2)
            elif isinstance(item, type) and issubclass(item, Action):
                children = self._register(item, urlpath_pat, has_params2)
            else:
                raise TypeError("%r: Action class expected" % (item,))
            if '{' in upath_pat:
                rexp_str = self._upath_pat2rexp(upath_pat, '', '(?=[/.]|$)')
                upath_rexp = re_compile(rexp_str)
                upath_prefix = upath_pat.split('{', 1)[0]
            else:
                upath_rexp = None
                upath_prefix = upath_pat
            tuples.append((upath_prefix, upath_rexp, children, None, None))
        return tuples

    def _register(self, action_class, base_upath_pat, has_params):
        action_method_mapping = getattr(action_class, '__mapping__')
        if action_method_mapping is None:
            raise ValueError("%s: There is no action method mapping." % action_class.__name__)
        tuples = []
        for upath_pat, action_methods in action_method_mapping:
            full_upath_pat = base_upath_pat + upath_pat
            self._all_urlpaths.append((full_upath_pat, action_class, action_methods))
            if '{' in upath_pat:
                rexp_str = self._upath_pat2rexp(upath_pat, '', '$')
                upath_rexp = re_compile(rexp_str)
                upath_prefix = upath_pat.split('{', 1)[0]
            elif has_params:
                upath_rexp = None
                upath_prefix = upath_pat
            else:
                self._fixed_urlpaths[full_upath_pat] = (action_class, action_methods)
                continue
            tupl = (upath_prefix, upath_rexp, None, action_class, action_methods)
            tuples.append(tupl)
        return tuples

    def lookup(self, req_urlpath):
        pargs = {}
        tupl = self._fixed_urlpaths.get(req_urlpath)
        if tupl:
            action_class, action_methods = tupl
            return action_class, action_methods, pargs
        return self._lookup(self._variable_urlpath_tuples, req_urlpath, pargs)

    def _lookup(self, tuples, req_path, pargs):
        for tupl in tuples:
            upath_prefix, upath_rexp, children, action_class, action_methods = tupl
            if not req_path.startswith(upath_prefix):
                continue
            #if not req_path.startswith(tupl[0]):
            #    continue
            #upath_prefix, upath_rexp, children, action_class, action_methods = tupl
            if upath_rexp:
                m = upath_rexp.match(req_path)
                if not m:
                    continue
                pargs.update(m.groupdict())
                remaining = req_path[m.end(0):]
                #pargs['id'] = req_path[1:]
                #remaining = ""
            else:
                remaining = req_path[len(upath_prefix):]
            if children:
                ret = self._lookup(children, remaining, pargs)
                if ret:
                    return ret
            elif remaining == "" and action_class:
                return action_class, action_methods, pargs
        return None

    def __iter__(self):
        return iter(self._all_urlpaths)


class ActionLazyMapping(ActionMapping):

    def __init__(self, mappings):
        self._all_urlpaths    = []
        self._fixed_urlpaths  = {}
        self._variable_urlpaths = []
        rexp_buf = self._nested_mappings = self._build(mappings, '', ['^'])
        rexp_buf.append('(?=[./]|$)')
        self._urlpath_rexp = re_compile("".join(rexp_buf))

    def _reorder_mappings(self, mappings):
        if not any( '{' in x[0] for x in mappings ):
            return mappings
        fn = lambda t, rx=self.URLPATH_PARAMETER_REXP: rx.sub('*', t[0])
        return sorted(mappings, key=fn, reverse=True)

    def _build(self, mappings, base_upath_pat, rexp_buf):
        rexp_buf.append('(?:')
        length = len(rexp_buf)
        for upath_pat, item in self._reorder_mappings(mappings):
            rexp_str = self._upath_pat2rexp(upath_pat, '', '', False)
            rexp_buf.append(rexp_str)
            n = len(rexp_buf)
            #
            full_upath_pat = base_upath_pat + upath_pat
            if isinstance(item, list):
                self._build(item, full_upath_pat, rexp_buf)
            else:
                action_class = item
                if '{' in full_upath_pat:
                    rexp_str = self._upath_pat2rexp(full_upath_pat, '^', '(?=[/.]|$)')
                    full_upath_rexp = re_compile(rexp_str)
                else:
                    full_upath_rexp = None
                t = [full_upath_pat, full_upath_rexp, action_class, None]
                self._variable_urlpaths.append(t)
                #
                rexp_buf.append('((?=[/.]|$))')
                #
                self._all_urlpaths.append((full_upath_pat, action_class))
            #
            if len(rexp_buf) == n:
                rexp_buf.pop()
            else:
                rexp_buf.append('|')
        #
        if rexp_buf[-1] == '|':
            rexp_buf.pop()
        if len(rexp_buf) == length:
            rexp_buf.pop()
        else:
            rexp_buf.append(')')
        return rexp_buf

    def lookup(self, req_urlpath):
        pair = self._fixed_urlpaths.get(req_urlpath)
        if pair:
            action_class, action_methods = pair
            return action_class, action_methods, {}
        #
        m = self._urlpath_rexp.match(req_urlpath)
        if not m:
            return None
        idx = m.groups().index('')
        tupl = self._variable_urlpaths[idx]
        base_upath_pat, base_upath_rexp, action_class, arr = tupl
        if isinstance(action_class, basestring):
            action_class = self._load_action_class(action_class)
            tupl[2] = action_class
        if base_upath_rexp:
            m = base_upath_rexp.match(req_urlpath)
            pargs = m.groupdict()
            remaining = req_urlpath[m.end(0):]
        else:
            pargs = None
            remaining = req_urlpath[len(base_upath_pat):]
        #
        if arr is None:
            arr = []
            found = None
            for upath_pat, action_methods in action_class.__mapping__:
                full_upath_pat = base_upath_pat + upath_pat
                if '{' not in full_upath_pat:
                    self._fixed_urlpaths[full_upath_pat] = (action_class, action_methods)
                    if upath_pat == remaining:
                        found = action_methods
                else:
                    rexp_str = self._upath_pat2rexp(upath_pat, '^', '$')
                    upath_rexp = re_compile(rexp_str)
                    arr.append([upath_rexp, action_methods])
            tupl[3] = arr
            if found:
                action_methods = found
                return action_class, action_methods, pargs or {}
        for upath_rexp, action_methods in arr:
            m = upath_rexp.match(remaining)
            if m:
                if pargs is None:
                    pargs = m.groupdict()
                else:
                    pargs.update(m.groupdict())
                return action_class, action_methods, pargs
        #
        return None

    def __iter__(self):
        for base_upath_pat, action_class in self._all_urlpaths:
            if isinstance(action_class, basestring):
                action_class = self._load_action_class(action_class)
            for upath_pat, action_methods in action_class.__mapping__:
                yield base_upath_pat + upath_pat, action_class, action_methods


class ActionHashedMapping(ActionMapping):

    def __init__(self, mappings):
        self._fixed_entries = {}
        self._variable_entries = []
        self._build(mappings, '')
        d, n = self._hashing(self._variable_entries)
        self._hashed_variable_entries = d
        self._prefix_length = n
        del self._variable_entries

    def _build(self, mappings, base_upath_pat):
        for upath_pat, item in mappings:
            curr_upath_pat = base_upath_pat + upath_pat
            if item is None:
                pass
            elif isinstance(item, list):
                self._build(item, curr_upath_pat)
            else:
                self._register(item, curr_upath_pat)

    def _register(self, action_class, curr_upath_pat):
        if isinstance(action_class, basestring):
            action_class = self._load_action_class(action_class)
        self._validate_action_class(action_class)
        for upath_pat, action_methods in action_class.__mapping__:
            full_upath_pat = curr_upath_pat + upath_pat
            if '{' in full_upath_pat:
                t = (full_upath_pat, action_class, action_methods)
                self._variable_entries.append(t)
            else:
                t = (action_class, action_methods)
                self._fixed_entries[full_upath_pat] = t

    def _calculate_hasing_index(self, upath_pats):
        pairs = [ (upath_pat.index('{'), upath_pat) for upath_pat in upath_pats ]
        indeces = sorted(set( idx for idx, _ in pairs ))
        sys.stderr.write("\033[0;31m*** debug: indeces=%r\033[0m\n" % (indeces, ))
        best_index = 0
        x = None
        for i in indeces:
            d = {}
            for idx, upath_pat in pairs:
                if  idx >= i:
                    s = upath_pat[:i]
                else:
                    s = None
                d[s] = d.get(s, 0) + 1
            n = max(d.values())
            if x is None or n <= x:
                _prev = (x, best_index)
                x = n
                best_index = i
                _curr = (x, best_index)
                sys.stderr.write("\033[0;31m*** debug: (x, best_index): %r => %r\033[0m\n" % (_prev, _curr))
            elif n > x:
                sys.stderr.write("\033[0;31m*** debug: n > x: %r > %r: break\033[0m\n" % (n, x))
                break
        return best_index

    def _hashing(self, variable_entries):
        upath_pats = ( t[0] for t in variable_entries )
        n = self._calculate_hasing_index(upath_pats)
        d = {}
        for urlpath_pat, action_class, action_methods in variable_entries:
            if urlpath_pat.index('{') >= n:
                prefix   = urlpath_pat[:n]
                rexp_str = self._upath_pat2rexp(urlpath_pat[n:], '', '$')
            else:
                prefix   = None
                rexp_str = self._upath_pat2rexp(urlpath_pat, '', '$')
            t = (re.compile(rexp_str), action_class, action_methods)
            d.setdefault(prefix, []).append(t)
        return d, n

    def __repr__(self):
        def _func_args(fn):
            return fn.__code__.co_varnames[:fn.__code__.co_argcount]
        def _inspect(action_methods, _args=_func_args):
            g = ( "%s: %s(%s)" % (meth, func.__name__, ', '.join(_args(func)[1:]))
                      for meth, func in action_methods.items() )
            return ", ".join(g)
        buf = []; add = buf.append
        add(    "<%s \n" % self.__class__.__name__)
        add(    "  _fixed_entries: {\n")
        for urlpath_pat, (action_class, action_methods) in self._fixed_entries.items():
            s1 = urlpath_pat
            s2 = action_class.__name__
            s3 = _inspect(action_methods)
            add("    %r:\n" % urlpath_pat)
            add("        (%s, {%s}),\n" % (s2, s3))
        add(    "  },\n")
        add(    "  _variable_entries: {\n")
        for key, tuples in self._hashed_variable_entries.items():
            add("    %r: [\n" % key)
            for t in tuples:
                urlpath_rexp, action_class, action_methods = t
                s1 = "rexp(%r)" % urlpath_rexp.pattern
                s2 = action_class.__name__
                s3 = _inspect(action_methods)
                add("        (%s, %s, {%s}),\n" % (s1, s2, s3))
            add("    ],\n")
        add(    "  },\n")
        add(    "  _prefix_length: %s,\n" % self._prefix_length)
        add(    ">")
        return "".join(buf)

    def lookup(self, req_urlpath):
        tupl = self._fixed_entries.get(req_urlpath)
        if tupl:
            action_class, action_methods = tupl
            return action_class, action_methods, {}
        #
        n = self._prefix_length
        prefix = req_urlpath[:n]
        tuples = self._hashed_variable_entries.get(prefix)
        if tuples:
            remaining = req_urlpath[n:]
        else:
            remaining = req_urlpath
            tuples = self._hashed_variable_entries.get(None)
        if tuples:
            for upath_rexp, action_class, action_methods in tuples:
                m = upath_rexp.match(remaining)
                if m:
                    return action_class, action_methods, m.groupdict()
        #
        return None


class ActionDFMMapping(ActionMapping):

    def __init__(self, mappings):
        self._build(mappings)

    def _build(self, mappings):
        self._fixed_entries    = {}
        self._variable_entries = {}
        def callback(full_urlpath, action_class, action_methods, _self=self):
            if '{' in full_urlpath:
                t = (action_class, action_methods)
                _self._register(full_urlpath, t, _self._variable_entries)
            else:
                t = (action_class, action_methods, ())
                _self._fixed_entries[full_urlpath] = t
        self._traverse(mappings, "", callback)

    def _traverse(self, mappings, base_urlpath, callback):
        for urlpath, target in mappings:
            if isinstance(target, list):
                self._traverse(target, base_urlpath + urlpath, callback)
            elif isinstance(target, type) and issubclass(target, BaseAction):
                action_class = target
                am = getattr(action_class, '__mapping__')
                if am is None:
                    raise NoActionMethodMappingError("%s: No functions decorated by '@on()'.")
                for upath, action_methods in am:
                    full_urlpath = base_urlpath + urlpath + upath
                    callback(full_urlpath, action_class, action_methods)
            else:
                raise NotActionClassError("%r: Action class expected." % (target,))

    def _register(self, full_path, t, dictionary):
        keys = self._KEYS_PER_TYPE
        rexp = self._URLPATH_PARAM_REXP
        d = dictionary
        for s in full_path[1:].split('/'):
            if '{' not in s:
                key = s
            else:
                m = rexp.match(s)
                if not m:
                    raise InvalidUrlpathParameterPatternError(
                        "%r: Invalid urlpath parameter patter." % (s,))
                name, type_name = m.groups()
                if type_name:
                    if not type_name.isalpha():
                        raise UnexpectedUrlpathParameterTypeError(
                            "%r: Expected urlpath parameter type name." % (s,))
                    key = keys.get(type_name)
                    if key is None:
                        raise UnknownUrlpathParameterTypeError(
                            "%r: Unknown paramter type name." % (s,))
                else:
                    int_p = name == 'id' or name.endswith('_id')
                    key = int_p and keys['int'] or keys['str']
            d = d.setdefault(key, {})
        #
        d[None] = t

    _KEYS_PER_TYPE      = {'int': 1, 'str': 2, 'path': 3}
    _URLPATH_PARAM_REXP = re.compile(r'^\{(\w*)(?::(.*)?)?\}$')

    def lookup(self, req_urlpath):
        t = self._fixed_entries.get(req_urlpath)
        if t:
            return t   # (action_class, action_methos)
        #
        key_inttype  = 1
        key_strtype  = 2
        key_pathtype = 3
        args = []; add = args.append
        d = self._variable_entries
        items = req_urlpath[1:].split('/')  # ex: '/x/y/1' => ('x','y','1')
        for s in items:
            if s in d:
                d = d[s]
            elif key_inttype in d and s.isdigit():
                d = d[key_inttype]
                add(int(s))
            elif key_strtype in d:
                d = d[key_strtype]
                add(s)
            elif key_pathtype in d:
                for i, x in enumerate(items):
                    if x is s:
                        break
                add("/".join(items[i+1:]))
                break
            else:
                return None    # not found
            if d is None:
                return None    # not found
        t = d.get(None)
        if not t:
            return None
        action_class, action_methods = t
        return (action_class,      # ex: HelloAction
                action_methods,    # ex: {'GET': do_show, 'PUT': do_update}
                args)              # ex: [123]


class Request(object):

    def __init__(self, env):
        self.env = env
        self.method = env['REQUEST_METHOD']
        self.path   = env['PATH_INFO'] or '/'

    @property
    def content_type(self):
        return self.env.get('CONTENT_TYPE')

    @property
    def content_length(self):
        return self.env.get('CONTENT_LENGTH')

    @property
    def wsgi_input(self):
        return self.env.get('wsgi.input')

    @property
    def wsgi_errors(self):
        return self.env.get('wsgi.errors')

    @property
    def headers(self):
        headers = getattr(self, '_headers', None)
        if headers is None:
            self._headers = headers = RequestHeaders(self.env)
        return headers

    def header(self, name):
        k = key.lower()
        if k == 'content-type':
            return self.env.get('CONTENT_TYPE')
        if k == 'content-length':
            return self.env.get('CONTENT_LENGTH')
        k = 'HTTP_' + k.upper().replace('-', '_')
        return self.env.get(k)


class RequestHeaders(object):

    def __init__(self, env):
        self.env = env

    def __getitem__(self, key):
        k = key.lower()
        if k == 'content-type':
            return self.env.get('CONTENT_TYPE')
        if k == 'content-length':
            return self.env.get('CONTENT_LENGTH')
        k = 'HTTP_' + k.upper().replace('-', '_')
        return self.env.get(k)

    def __iter__(self):
        env = self.env
        if 'CONTENT_TYPE' in env:
            yield 'Content-Type'
        if 'CONTENT_LENGTH' in env:
            yield 'Content-Length'
        for k in env:
            if k.startswith('HTTP_'):
                yield k[5:].title().replace('_', '-')

    def items(self):
        env = self.env
        if 'CONTENT_TYPE' in env:
            yield 'Content-Type', env['CONTENT_TYPE']
        if 'CONTENT_LENGTH' in env:
            yield 'Content-Length', env['CONTENT_LENGTH']
        for k in env:
            if k.startswith('HTTP_'):
                yield k[5:].title().replace('_', '-'), env[k]


class Response(object):

    __slots__ = ('status_code', 'header_list', 'body')

    def __init__(self):
        self.status_code = 200
        self.header_list = [
            ('Content-Type',   None),
            ('Content-Length', None),
        ]
        self.body = None

    @property
    def status(self):
        return HTTP_STATUS_DICT[self.status_code]

    @property
    def content_type(self):
        return self.header_list[0][1]

    @content_type.setter
    def content_type(self, value):
        self.header_list[0] = ('Content-Type', value)

    @property
    def content_length(self):
        return int(self.header_length[0][1])

    @content_length.setter
    def content_length(self, value):
        self.header_list[1] = ('Content-Length', str(value))

    def get_header(self, name):
        if name == 'Content-Type':
            return self.content_type
        if name == 'Content-Length':
            return self.content_length
        for k, v in self.header_list:
            if k == name:
                return v
        return None

    def set_header(self, name, value):
        if name == 'Content-Type':
            self.content_type = value
            return self
        if name == 'Content-Length':
            self.content_length = value
            return self
        for i, (k, _) in enumerate(self.header_list):
            if k == name:
                break
        else:
            self.header_list.append((name, value))
            return self
        self.header_list[i] = (name, value)
        return self

    def add_header(self, name, value):
        self.header_list.append((name, value))

    def get_header_list(self):
        arr = self.header_list
        if arr[1][1] is None:
            arr.pop(1)
        if arr[0][1] is None:
            arr.pop(0)
        self.header_list = None
        return arr

    def add_cookie(self, name, value, domain=None, path=None, max_age=None, expires=None,
                   httponly=None, secure=None):
        buf = []; add = buf.append
        add("%s=%s" % (name, value))
        if domain:   add("; Domain=%s"  % domain)
        if path:     add("; Path=%s"    % path)
        if max_age:  add("; Max-Age=%s" % max_age)
        if expires:  add("; Expires=%s" % expires)
        if httponly: add("; HttpOnly")
        if secure:   add("; Secure")
        self.header_list.append(('Set-Cookie', ''.join(buf)))


class WSGIApplication(object):

    REQUEST  = Request
    RESPONSE = Response

    def __init__(self, mappings, _=None, lazy=False, hashing=None):
        if _ is not None:
            raise TypeError("%r: Unexpected 2nd argument for %s()." % (_, self.__class__.__name__))
        if isinstance(mappings, ActionMapping):
            self.mapping = mappings
        elif lazy:
            self.mapping = ActionLazyMapping(mappings)
        elif hashing:
            self.mapping = ActionHashedMapping(mappings)
        else:
            self.mapping = ActionEagerMapping(mappings)

    def lookup(self, req_urlpath):
        return self.mapping.lookup(req_urlpath)

    def each_mapping(self):
        return iter(self.mapping)

    def show_mapping(self):
        req_methods = ActionMapping.REQUEST_METHODS + ['ANY']
        buf = []; add = buf.append
        for urlpath_pat, action_class, action_methods in self.each_mapping():
            lst = [ "%s: %s()" % (k, action_methods[k].__name__)
                      for k in req_methods if k in action_methods ]
            add("- urlpath:  %s\n" % urlpath_pat)
            add("  class:    %s\n" % action_class.__name__)
            add("  methods:  {%s}\n" % ", ".join(lst))
            add("\n")
        return "".join(buf)

    def __call__(self, env, start_response):
        status, headers, body = self.handle_request(env)
        start_response(status, headers)
        try:
            return body
        finally:
            if hasattr(body, 'close'):
                body.close()

    def handle_request(self, env):
        req  = self.REQUEST(env)
        resp = self.RESPONSE()
        tupl = self.lookup(req.path)
        if tupl is None:
            return self.error_4xx(404, env)
        action_class, action_methods, action_args = tupl
        #
        req_meth = req.method
        action_func = action_methods.get(req_meth)
        if not action_func:
            if req_meth == 'HEAD':
                req_meth = action_methods.get('HEAD') or action_methods.get('ANY')
            else:
                req_meth = action_methods.get('ANY')
            if not action_func:
                return self.error_4xx(405, env)
        #
        action_obj = action_class(req, resp)
        try:
            body = action_obj.run_action(action_func, action_args)
            return resp.status, resp.get_header_list(), body
        except HttpException as ex:
            return self.handle_http_exception(ex, req, resp)
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            return self.handle_exception(ex, req, resp)

    def error_4xx(self, status_code, env):
        status = HTTP_STATUS_DICT[status_code]
        html = u"""<h2>%s</h2>""" % status
        binary = html.encode(ENCODING)
        headers = [
            ('Content-Type',   "text/html;charset=utf-8"),
            ('Content-Length', str(len(binary))),
        ]
        return status, headers, [binary]

    def handle_http_exception(self, ex, req, resp):
        status_code = ex.status_code
        content = B(status_code)
        headers = req.headers
        headers.setdefault('Content-Type',   "text/plain;charset=utf-8")
        headers.setdefault('Content-Length', str(len(content)))
        return status, tuple(resp.generate_header_pairs()), [content]

    def handle_exception(self, ex, req, resp):
        #stderr = req.env['wsgi.errors']
        stderr = sys.stderr
        sys.stderr.write(traceback.format_exc())
        #
        status_code = 500
        status = HTTP_STATUS_DICT[status_code]
        html = u"""<h2>%s</h2>""" % status
        binary = html.encode(ENCODING)
        headers = [
            ('Content-Type',   "text/html;charset=utf-8"),
            ('Content-Length', str(len(binary))),
        ]
        return status, headers, [binary]


def mock_env(req_meth, req_urlpath, _=None, query=None, form=None, json=None,
             headers=None, cookies=None, env=None):
    global BytesIO
    try:
        from io import BytesIO
    except ImportError:
        from cStringIO import StringIO as BytesIO
    if _ is not None:
        raise TypeError("mock_env(): 'query' argument should be specfied as keyword argument.")
    if env is None:
        env = {}
    if req_meth:
        env['REQUEST_METHOD'] = S(req_meth)
    if req_urlpath:
        env['PATH_INFO'] = S(req_urlpath)
    if query:
        env['QUERY_STRING'] = S(_build_query_string(query))
    if form:
        env['wsgi.input'] = BytesIO(B(_build_query_string(query)))
    if json:
        import json as json_
        json_str = json_.dumps(json)
        env['wsgi.input'] = BytesIO(B(json_str))
    if headers:
        for k in headers:
            v = headers[k]
            if k.lower() == 'content-type':
                env['CONTENT_TYPE'] = S(v)
            elif k.lower() == 'content-length':
                env['CONTENT_LENGTH'] = S(str(v))
            else:
                env['HTTP_' + k.upper().replace('-', '_')] = S(v)
    if cookies:
        env['HTTP_COOKIE'] = S(_build_cookie_string(cookie))
    #
    global setup_testing_defaults
    if setup_testing_defaults is None:
        from wsgiref.util import setup_testing_defaults
    setup_testing_defaults(env)
    return env

def _build_query_string(query):
    if isinstance(query, (unicode, binary)):
        return query
    if isinstance(query, dict):  # TODO: percent encode
        return '&'.join("%s=%s" % (k, query[k]) for k in query)
    raise TypeError("%r: failed to build query string." % (query,))

def _build_cookie_string(cookie):
    if isinstance(cookie, (unicode, binary)):
        return cookie
    if isinstance(cookie, dict):  # TODO: percent encode
        return '; '.join("%s=%s" % (k, cookie[k]) for k in cookie)
    raise TypeError("%r: failed to build cookie string." % (cookie,))


class StartResponse(object):

    def __init__(self):
        self.status  = None
        self.headers = None

    def __call__(self, status, headers):
        self.status = status
        self.headers = headers
