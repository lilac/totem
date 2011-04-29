from os import path

# Django settings for sweetter project.
BASEDIR = path.dirname(path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Daniel Garcia Moreno', 'dani@danigm.net'),
)

DOMAIN = 'http://tot2me.com'

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = path.join(BASEDIR, 'tot2me.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''               # Not used with sqlite3.
DATABASE_PASSWORD = ''           # Not used with sqlite3.
DATABASE_HOST = ''               # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''               # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(BASEDIR, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'om7odj)f4_bn-djy!^tdw2!!49ip+86e98#0-(#*vzg@x4sqag'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'flash.context_processor',
    'ublogging.contexts.profile',
    'ublogging.contexts.flatpages',
)

INTERNAL_IPS = ('127.0.0.1',
    '114.215.28.59' )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

AUTH_PROFILE_MODULE = 'ublogging.Profile'

LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    path.join(BASEDIR, 'templates'),
)

SERIALIZATION_MODULES = {
    'fjson': 'util.full_serializers.json',
    'sjson': 'util.serializers.json'
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'django.contrib.webdesign',

    'ublogging',
    'contrib.userform',
    'contrib.groups',
    'contrib.recoverpw',
    'contrib.karma',
    'contrib.followers',
    'contrib.replies',
    'contrib.remove',
    'contrib.shorturl',
    'contrib.privatetimeline',
    'contrib.spam',
    
    'contrib.api',
    'jabberbot',
)

INSTALLED_PLUGINS = (
    #'contrib.userform.UserForm.UserForm',
    'contrib.spam.plugin.Spam',
    'contrib.privatetimeline.PrivateTimelinePlugin.PrivateTimelinePlugin',
    'contrib.replies.RepliesPlugin.RepliesPlugin',
    'contrib.groups.GroupsPlugin.GroupHooks',
    'contrib.recoverpw.recoverplugin.Recover',
    'contrib.karma.KarmaPlugin.KarmaCount',
    'contrib.followers.FollowerPlugin.FollowingList',
    'contrib.followers.FollowerPlugin.FollowerList',
    'contrib.remove.RemovePlugin.RemovePlugin',
    'contrib.shorturl.plugin.ShortUrlPlugin',
    'jabberbot.jabberplugin.JabberPlugin',
)

LOGIN_URL = "/login"

POST_PER_PAGE = 20

# Jabberbot

JB_USER = "sbottest@jabberes.org"
JB_PASSWD = "..."

# email config
EMAIL_HOST = 'smtp.sina.cn'
EMAIL_PORT = ''
EMAIL_HOST_USER = 'autoreminder@sina.cn'
EMAIL_HOST_PASSWORD = 'sysu123'

MSG_FROM = "autoreminder@sina.cn"
CONFIRMATION_MSG = """
Tot2me 0.1 validation
======================

Hi %(username)s!

This email account is registered in tot2me 0.1, if you don't
register in that web service you can ignore that.

To validate your account follow this link:

http://www.tot2me.com:8000/sweetter/validate/%(apikey)s

--
tot2me team

"""

RECOVERY_MSG = """
Tot2me 0.1 pw recovery
=======================

Hi %(username)s!

Your receive this email because you are trying to recover your
sweetter password. If you don't ask for a password recovery then
ignore that email.

To recover your tot2me password follow this link:

http://www.tot2me.com:8000/recover/validate/%(key)s

--
tot2me team

"""

