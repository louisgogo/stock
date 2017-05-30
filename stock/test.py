import zipfile
import re

td = "document.write('52.43.82.228')"
ip = re.search("'(.*)'", td).group(1)
print(ip)
