import re



url = 'https://www.qu.la/book/394/10612920.html'
url1 = 'https://www.qu.la/10612920.html'
re_url = re.compile('.*book.*?')
if re_url.match(url1):
    print(re_url.match(url))
    print('true')
else:
    print(re_url.match(url1))
    print('false')