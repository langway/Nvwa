
from loongtian.util.helper import jsonplus as json
from datetime import datetime
if __name__=="__main__":
    print (json.dumps(u"unicode"))
    print (json.dumps((23, u"unicode")))
    print (json.dumps({"x": [4, 3], "y": (23, u"unicode"), "z": set(["a", u"u"]), "t": datetime.now()}))
