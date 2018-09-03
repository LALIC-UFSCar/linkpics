from urllib.parse import urlparse


#get domain name

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-5] + '.' + results[-4] + '.' + results[-3]
    except:
        return ''



def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

