import sys,re
open(sys.argv[2],'a+').write('\n'.join(str(email) for email in set(re.findall("[\w\+\._]+@\w+[\w*\.]{1,}\w+",open(sys.argv[1],'r').read()))));
