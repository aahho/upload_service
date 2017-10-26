import env, uuid, pygeoip, os, bcrypt, random, datetime, magic, re
from werkzeug.utils import secure_filename

##
# To fetch from environment variable file
##
def getenv(key):
    return env.getKey(key)

##
# To generate unique code
# uuid package
##
def generate_uuid():
    return uuid.uuid4()

##
# GET USER IP ADDRESS FROM REQUEST
##
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

##
# To get requested ip current location
# Reference http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
##
def fetch_location(request):
    ip = get_client_ip(request)
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    collection = pygeoip.GeoIP(BASE_PATH+'/GeoLiteCity.dat')
    return collection.record_by_name(ip)

##
# To hash the access-token
##
def generate_hash_token():
    return bcrypt.hashpw(str(random.random()), bcrypt.gensalt())

##
# To hash the password while storing or restoring password
##
def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

##
# To validate/comapre the hash password
# @param present - user's account present password
# @param requested - password requested for verification
##
def validate_hash_password(requested, present):
    return bcrypt.checkpw(str(requested), str(present))

##
# To start a new session when user logs in
##
def generate_new_session(request, token):
    if 'token' in request.session:
        del request.session['token']
    request.session['token'] = token.access_token
    return True
##
# To get current month and year
##
def get_current_month_and_year():
    return datetime.date.today().strftime("%B")+datetime.date.today().strftime("%Y")

##
# Get File Name
##
def get_file_name(file):
    split = datetime.datetime.now().strftime("%c")+str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))
    trim = re.sub('[\s+]', '', split)
    return re.sub(':', '', trim)+os.path.splitext(secure_filename(os.path.basename(file.name)))[1]

##
# Get File Extension
##
def get_file_extension(file):
    return os.path.splitext(secure_filename(os.path.basename(file.name)))[1]

##
# Get File Title
##
def get_file_title(file):
    return os.path.splitext(secure_filename(os.path.basename(file.name)))[0]

##
# Get File MIME Type
##
def get_mime_type(file):
    return magic.from_file(getenv('UPLOAD_FOLDER')+'/'+secure_filename(os.path.basename(file.name)), mime=True)

##
# Get File Path Where File gets uploaded on server
##
def get_file_path(file):
    return getenv('UPLOAD_FOLDER')+'/'+secure_filename(os.path.basename(file.name))

##
# To fetch postgresql database url
##
def generate_pgsql_connect_url():
    return getenv('DB_PSQL')+'://'+getenv('DB_USERNAME')+':'+getenv('DB_PASSWORD')+'@localhost/'+getenv('DB_NAME')

##
# To fetch mongo database url
##
def generate_mongo_connect_url():
    return 'mongodb://'+getenv('HOST')+':'+str(getenv('MONGO_PORT'))+'/'+getenv('MONGO_DB')

##
# Get File Size in MB
##
def get_file_size(file):
    return os.path.getsize(get_file_path(file))/1024

##
# Get Allowed Extension
##
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'xls', 'csv']
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
