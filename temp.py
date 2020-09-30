import platform
import mechanize
import urllib.parse
import brotli
import re
import yaml


def getstats():
    csrf = ''
    final = []
    user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    if platform.system() == 'Windows':
        with open(r'data.yml') as file:
            username = yaml.load(file, Loader=yaml.FullLoader)['username']
        with open(r'data.yml') as file:
            password = yaml.load(file, Loader=yaml.FullLoader)['password']
    elif platform.system() == 'Linux':
        with open(r'/home/pi/git/NW-Bot/data.yml') as file:
            username = yaml.load(file, Loader=yaml.FullLoader)['username']
        with open(r'/home/pi/git/NW-Bot/data.yml') as file:
            password = yaml.load(file, Loader=yaml.FullLoader)['password']            


    browser = mechanize.Browser()
    browser.set_handle_robots( False )
    browser.addheaders = [('User-agent', user)]
    browser.open("https://panel.apexminecrafthosting.com/site/login")
    browser.select_form(nr = 0)
    control = browser.form.find_control("YII_CSRF_TOKEN")
    csrf = urllib.parse.quote(control.value)
    browser.form['LoginForm[name]'] = username
    browser.form['LoginForm[password]'] = password
    browser.submit()


    data='ajax=refresh&type=all&log_seq=0&YII_CSRF_TOKEN=' + csrf
    req = mechanize.Request('https://panel.apexminecrafthosting.com/server/312215', data=data)
    req.add_header("user-agent", user)
    req.add_header("accept-encoding","gzip, deflate, br")
    browser.cookiejar.add_cookie_header(req)
    raw = mechanize.urlopen(req).read()
    decoded = brotli.decompress(raw).decode("utf-8")
    cpudat = re.search("(\d+)[%] CPU",decoded).group().split('%', 1)
    ramdat = re.search("(\d+)[%] MEM",decoded).group().split('%', 1)

    final.append(cpudat[0])
    final.append(ramdat[0])
    return final