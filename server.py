from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse,parse_qs
from html import escape
from zipfile import ZipFile
import glob
import os

folderprefix = 'F:/myExt/fu/'
pagebase = '/'
imageformats = ('jpg','png','jpeg','gif')

with open(os.path.dirname(os.path.abspath(__file__))+"/template_listfile.html","r",encoding="utf8") as a_file:
    template_listfile = a_file.read()
with open(os.path.dirname(os.path.abspath(__file__))+"/template_lazyphoto.html","r",encoding="utf8") as a_file:
    template_lazyphoto = a_file.read()

def getImage(zip,n):
    try:
        with ZipFile(folderprefix+zip, 'r') as myzip:
            filename = myzip.namelist()[int(n)]
            sub_filename = filename.split('.')
            return myzip.read(filename),sub_filename[-1]
    except Exception as e:
        raise IOError('Zip file error : ' + str(e))
	#pass

def getFilelist():
    filelist = glob.glob(folderprefix+'./**/*.zip',recursive=True)
    filelist = ['<a href="{0}?path={1}">{1}</a>'.format(pagebase,escape(os.path.relpath(x, start=folderprefix))) for x in filelist]
    return template_listfile.format(filelist='<br>'.join(filelist))
	
def getLazyphoto(path):
    try:
        with ZipFile(folderprefix+path, 'r') as myzip:
            o = []
            for i,a in enumerate(myzip.namelist()):
                if a.split('.')[-1] in imageformats:
                    o.append(i)
        PICtoJS = ['{}?zip={}&n={}'.format(pagebase,path,str(i)) for i in o]
        return template_lazyphoto.format(PICtoJS=PICtoJS,path=path)
    except Exception as e:
        raise IOError('Zip file error : ' + str(e))


class S(BaseHTTPRequestHandler):
    def _set_headers_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def _set_headers_image(self,type):
        if type not in imageformats:
            raise IOError('Error image format')
            return False
        self.send_response(200)
        self.send_header('Content-type', 'image/'+type)
        self.end_headers()
        return True
    
    def parseQuery(self,item):
        return parse_qs(urlparse(self.path).query).get(item, None)

    def do_GET(self):
        # zip,n -> getImage(zip,n)
        # [] -> getFilelist()
        # path -> getLazyphoto(path)
        try:
            q_zip = self.parseQuery("zip")
            q_n = self.parseQuery("n")
            q_path = self.parseQuery("path")
            if q_path is not None:
                res = getLazyphoto(q_path[0])
                self._set_headers_html()
                self.wfile.write(res.encode("utf-8"))
            elif q_zip is not None and q_n is not None:
                try:
                    q_n = int(q_n[0])
                except ValueError:
                    raise IOError("Index error")
                fp ,type = getImage(q_zip[0],q_n)
                if self._set_headers_image(type):
                    self.wfile.write(fp)
            else:
                res = getFilelist()
                self._set_headers_html()
                self.wfile.write(res.encode("utf-8"))
        except IOError as e:
            self.send_error(404,'File Not Found : '+str(e))

    def do_HEAD(self):
        self._set_headers_html()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers_html()
        self.wfile.write("posted".encode("utf-8"))
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    try:
        httpd.serve_forever()
    except RuntimeError as e:
        print(str(e))
        httpd.shutdown()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
