from bs4 import BeautifulSoup
import requests as req
import os

_name = input("Input name of package: ")
_version = input("Input version: ")
GRAPH = 'digraph G {\n'
_used = ['django']

def doGraph(name, version):
    global GRAPH
    global _used
    
    resp = req.get("https://pypi.org/simple/" + name + '/')
    soup = BeautifulSoup(resp.text, 'lxml')
    
    stri = name + '-' + version
    
    links= soup.find_all('a')
    
    list = []
    for EachPart in soup.select('a'):
        txt = EachPart.get_text()
        txt = txt[::-1] #reverse and let it costil'
        if txt[0] == 'l' and txt[1] == 'h' and txt[2] == 'w':
            list.append(EachPart)
            
    if len(list) == 0:
        return
            
    lst = []    
    if version != "0":
        m = 1
        for i in list:
            ttt = i.get_text()
            j = len(name)
            f = True
            for y in version:
                if ttt[j+1] != y:
                    f = False
                j+=1
            if (f == True):
                #print(str(m) + " " + i.get_text())
                lst.append(i)
                m+=1
    else:
        lst.append(list[-1])
        
    chosen = lst[-1]
    
    #chosen = 0        
    #if len(lst) != 1:
    #    st = int(input("Chose your version: "))
    #    chosen = lst[st - 1]
    #else:
    #    chosen = lst[0]
        
    url = chosen.attrs["href"]
    fo = open("wd/" + chosen.get_text(), "wb")
    ufr = req.get(url)
    fo.write(ufr.content)
    fo.close()  
    
    #os.system("pip wheel unpack " + chosen.get_text())
    
    import zipfile
    archive = zipfile.ZipFile("wd/" + chosen.get_text(), 'r')
    archive.extractall("wd/")
    
    metad_ = ''
    
    ere = ""
    for op in range(0, len(name)):
        if name[op] == '-':
            ere += "_"
        else:
            ere += name[op]
    name = ere
    
    file_list = os.listdir("wd/")
    for tyt in file_list:
        if (".dist-info" in tyt) and ((name.lower() + "-") in tyt.lower()):
            metad_ = tyt
    
    metad = open("wd/" + metad_ + "/METADATA", "r")
    #print("wd/" + metad_ + "/METADATA")
    
    for line in metad:
        if "extra" in line :
            continue
        
        if "Requires-Dist:" in line:
            re = ""
            fl = 0
            for syma in range(0, len(line)):
                sym = line[syma]
                
                if fl == 2 and sym != ' ' and sym != '(' and sym != '[':
                    re += sym
                    if syma == len(line)-2:
                        break
                elif fl == 2 and (sym == ' ' or sym == '(' or sym == '['):
                    break
                
                if sym == ':':
                    fl += 1
                elif sym == ' ' and fl == 1:
                    fl += 1
            
            strre = '\"' + name + '\" -> \"' + re + '\"' + '\n'
            GRAPH += strre
            
            doGraph(re, "0")
            
            #if not(re in _used):
            #    _used.append(re)
            #    doGraph(re, "0") 
    
    
doGraph(_name, _version)

GRAPH += '}'
print(GRAPH)