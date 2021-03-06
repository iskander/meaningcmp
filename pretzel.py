#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

from mncmp import mncmp
from sys import argv
from sys import stdout
from os import system
import readline
from cmd import Cmd

class Pretzel(Cmd):
    def __init__(self):
        self.pretzel_keys = []
        self.prompt = '> '
        self.completekey = None
        self.cmdqueue = []
        self.stop = False
        self.stdout = stdout
        self.minsim = 0.34
        print "Loading data... ",
        stdout.flush()
        try:
            if len(argv)==2:
                self.datafile = argv[1]
            else:
                self.datafile = "pretzel.dat"
            f = open(self.datafile)
            str = f.readline()
            while str and len(str) is not 0:
                if str[-1]=='\n':
                    str = str[:-1]
                self.pretzel_keys.append([str[:str.find(':')],str[str.find(':')+1:]])
                str = f.readline()
            print "[done]"
        except:
            self.pretzel_keys.append(['hello','hi'])
            self.pretzel_keys.append(['how are you','fine, thanks'])
            self.pretzel_keys.append(['exit','exit'])
            self.pretzel_keys.append(['quit','quit'])
            print "[failed] (new database will be created in pretzel.dat after a clean exit (type exit to do that))"
        print "Initializing mncmp()... ",
        stdout.flush()
        mncmp("doors","walls") # need to pass anything through it once so that the wordnet dictionnaries get loaded etc.
        print "[done]"

    def flushdb(self):
        f = open(self.datafile,"w")
        for item in self.pretzel_keys:
            f.write(item[0]+":"+item[1]+"\n")
        f.close()

    def panic(self):
        print "I don't know what to do!"
        return raw_input("Please enter desired response (simple text, /shell command, or /python command): ")

    def execute(self,cmd):
        if len(cmd)==0:
            return
        if cmd=='exit' or cmd=='quit':
            self.stop = True
            return
        if cmd[0]=='/':
            if cmd[1:7]=='shell ':
                system(cmd[7:])
            elif cmd[1:8]=='python ':
                exec(cmd[8:])
        else:
            print cmd

    def postcmd(self, stop, line):
        return self.stop

    def do_help(self, args):
        self.default('help '+args)

    def default(self, user):
        success = False
        for item in self.pretzel_keys:
            args = mncmp(user,item[0],self.minsim)
            itemtmp = item[1]
            if args is not False:
                if args is not True:
                    # means we have some arguments
                    for x in range(0,len(args)):
                        try:
                            itemtmp = itemtmp.replace('arg'+repr(x+1),args[x])
                        except:
                            pass
                success = True
                self.execute(itemtmp)
                break
        if not success:
            cmd = self.panic()
            if cmd!="":
                self.pretzel_keys.append([user,cmd])
            else:
                print "Received empty input; not adding to database."

        self.flushdb()

p = Pretzel()        
p.cmdloop()
