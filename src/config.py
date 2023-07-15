import redis

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#)=h)_wc*k%f=wk+!$x0t%1wx7*_50$a1%*75s$og(8$27$ju1'
EXEMPT_BP = {"rega", "profa", "groca"}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_TYPE = 'redis'
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True
SESSION_REDIS = redis.from_url(url="redis://:j7+jOomYiIP6APPxSBaxR8vcmqjkPnknGN0GHDEmYF3z9ChJ10XkIJPmN5k0ql5PlY60TXiW0AVDQv13@localhost:6379", db=3)

ALLOWED_HOSTS = ['127.0.0.1', '.cfe.sh', 'localhost']
LOGIN_URL = "/login"

# EVENTS SETTINGS: environment variables for events
MAX_SPOT_LENGTH = 400
EVENT_ACTION_OPTIONS = ("reaction", "ref", "response")
EVENT_UPLOADS = '/events_uploads'

# VOICE SETTINGS: environment variables for voice
VOICE_ACTION_OPTIONS = ("like", "comment", "ref")
VOICE_UPLOADS = '/voice_uploads'


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'mp4', 'webm', 'mp3', 'ogg'}