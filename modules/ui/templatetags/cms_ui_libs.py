import os, json, logging
from django import template
from django.conf import settings

_log = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag(takes_context=True)
def require_ui_lib(context, lib):
    ''' Include a bower compontents and all it's dependencies '''
    # Keep track of dependencies discovered to avoid duplicate dependencies being added, at least within same context
    libs = context.get('_require_ui_libs',[])
    context['_require_ui_libs'] = libs
    files = _get_lib_files(lib, exclude=libs)
    libs += files
    return '<!-- %s -->\n%s' % (lib,_get_files_html(files))

@register.simple_tag
def require_ui_file(path):
    ''' Includes a single file. We don't check if it actually exists '''
    return _get_path_tag(os.path.join(settings.STATIC_ROOT, settings.JS_COMPONENTS_DIR, path))


# Utils

def _get_lib_files(name, version=0, libs=None, exclude=[]):
    '''
    No way to know what optional files of JS modules to include. Use require_ui_file for that.
    '''
    if libs is None:
        libs = []
    rpath = os.path.join(settings.STATIC_ROOT, settings.JS_COMPONENTS_DIR, name)
    
    if os.path.exists(rpath):

        # find package file
        for p in ('bower.json','package.json'):
            pkg_file = os.path.join(rpath, p)
            if os.path.exists(pkg_file):
                break

        # parse package
        with open(pkg_file,'r') as f:
            # We could validate version but should have been done already by bower
            pkg = json.loads(f.read())

            # load dependencies first
            deps = pkg.get('dependencies',{})
            for name, ver in deps.items():
                _get_lib_files(name, ver, libs, exclude)

            # See what files are apparently important
            main_files = pkg['main']
            if type(main_files) is not list:
                main_files = [main_files]

            for mf in main_files:
                # Cheap way to ignore .less files, etc
                if mf.endswith('.js') or mf.endswith('.css'):
                    mfp = os.path.join(rpath,mf.strip('./'))
                    # Make sure this lib is not already in the list
                    if mfp not in libs and mfp not in exclude:
                        libs.append(mfp)
    else:
        _log.error('Could not find lib %s' % name)
    return libs

def _get_files_html(files):
    js_html = ''
    css_html = ''
    for path in files:
        if path.endswith('.css'):
            css_html += _get_path_tag(path)
        elif path.endswith('.js'):
            js_html += _get_path_tag(path)
    return (css_html+js_html).strip()

def _get_path_tag(path):
    js_tag = '<script src="%s"></script>\n'
    css_tag = '<link rel="stylesheet" href="%s">\n'
    path = (settings.STATIC_URL + path.replace(settings.STATIC_ROOT,'')).replace('//','/').replace('\\','/')
    if path.endswith('.css'):
        return css_tag % path
    elif path.endswith('.js'):
        return js_tag % path
    else:
        _log.error("Not sure what this file is: %s" % path)
        return "<!-- Unknown file type: %s -->" % path




# This is a multiline tag that will take a string of mulitple lines with names of libs.
# Something we might want to play with later for compressing when including mulitple libs 

# @register.tag
# def require_ui_libs(parser, token):
#     ''' This magical tag removes duplicate dependencies within files included from an instance of this tag. Using require_ui_lib won't do that '''
#     nodelist = parser.parse(('endrequire_ui_libs',))
#     parser.delete_first_token()
#     return RequireLibs(nodelist)

# class RequireLibs(template.Node):
#     def __init__(self, nodelist):
#         self.nodelist = nodelist

#     def render(self, context):
#         text = self.nodelist.render(context)
#         items = [i.strip() for i in text.strip().split("\n")]
#         print "items:", items
#         output = ''
#         libs = []
#         for name in items:
#             _get_lib_files(name, libs=libs)
#         return _get_files_html(libs)
