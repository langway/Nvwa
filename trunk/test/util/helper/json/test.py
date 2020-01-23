
from loongtian.util.helper import jsonplus as json
from datetime import datetime
if __name__=="__main__":
    print (json.dumps("unicode"))
    print (json.dumps((23, "unicode")))
    print (json.dumps({"x": [4, 3], "y": (23, "unicode"), "z": set(["a", ""]), "t": datetime.now()}))
