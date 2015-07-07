import os, json, logging
from django import template
from django.conf import settings

_log = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag(takes_context=True)
def require_ui_lib(context, lib):
    return _require_ui_lib(context, lib)

# following 2 tags are meant to separate css and js, if places in different sections or 
# need to be split in order to be compressed  
@register.simple_tag(takes_context=True)
def require_ui_css(context, lib):
    return _require_ui_lib(context, lib, filter_type=('.css',))

@register.simple_tag(takes_context=True)
def require_ui_js(context, lib):
    return _require_ui_lib(context, lib, filter_type=('.js',))


@register.simple_tag
def require_ui_file(path):
    ''' Includes a single file. We don't check if it actually exists '''
    return _get_path_tag(os.path.join(settings.STATIC_ROOT, settings.JS_COMPONENTS_DIR, path))


# Utils

def _require_ui_lib(context, lib, filter_type=('.js','.css')):
    ''' Include a bower compontents and all it's dependencies '''
    # Keep track of dependencies discovered to avoid duplicate dependencies being added, at least within same context
    libs_var = '_require_ui_libs'
    
    libs = context.get(libs_var,[])
    context[libs_var] = libs
    files = _get_lib_files(lib, exclude=libs, filter_type=filter_type)
    libs += files
    if files:
        html = _get_files_html(files)
    else:
        html = '<script>if (window.console) console.error("_require_ui_lib: Could not find library named \'%s\'. filter_type=%s");</script>' % (lib,filter_type)
    return '<!-- %s -->\n%s' % (lib,html)


def _get_lib_files(name, version=0, libs=None, exclude=[], filter_type=('.js','.css')):
    '''
    No way to know what optional files of JS modules to include. Use require_ui_file for that.
    '''
    if libs is None:
        libs = []

    comps_dir = os.path.join(settings.STATIC_ROOT, settings.JS_COMPONENTS_DIR)
    lib_path = os.path.join(comps_dir, name)

    if os.path.exists(lib_path):

        # find package file
        for p in ('bower.json','package.json'):
            pkg_file = os.path.join(lib_path, p)
            if os.path.exists(pkg_file):
                break

        # parse package
        with open(pkg_file,'r') as f:
            # We could validate version but should have been done already by bower
            pkg = json.loads(f.read())

            # load dependencies first
            deps = pkg.get('dependencies',{})
            for name, ver in deps.items():
                _get_lib_files(name, ver, libs, exclude, filter_type=filter_type)

            # See what files are apparently important
            main_files = pkg.get('browser', pkg.get('main',[]))
            if not main_files:
                _log.error("Don't know what files to include for %s" % name)
                return libs
            elif type(main_files) is not list:
                main_files = [main_files]

            # Our extension of bower.json lets us specificy individual files from other libs to include
            file_deps = [os.path.join(comps_dir,cf.strip('./')) for cf in pkg.get('cms_file_dependencies',[])]

            # make sure file_deps are listed before main files
            main_files = file_deps + [os.path.join(lib_path,mf.strip('./')) for mf in main_files]
            

            for mf in main_files:
                # Cheap way to ignore .less files, etc
                if not filter_type or any([mf.endswith(t) for t in filter_type]):
                    # Make sure this lib is not already in the list
                    if mf not in libs and mf not in exclude:
                        print "mf:", mf
                        libs.append(mf)
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
