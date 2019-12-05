import re, os, platform
from sys import stdout
from datetime import datetime

class Functions:
    system = platform.system()
    root_path = os.getcwd()

    #if system == 'Linux':
    root_path += '/'

    def contains_word(self, s, *args):
        for w in args:
            if f' {w} ' in f' {s} ':
                return True

        return False

    def replace_words(self, message, s, *args):
        for w in args:
            #message = message.replace(w, s)
            # pattern = re.compile(w, re.IGNORECASE)
            #print(pattern)

            #message = pattern.sub(s, message)
            message = re.sub(r"\b%s\b" % w, s, message, flags=re.I) #'bye bye bye'
            # print(message)
            #message = re.sub(r"\b%s\b".lower() % w.lower() , s, message)

        message = message.strip()
        
        return message

    def get_time(self):
        return datetime.now().strftime('%X')

    def get_time_and_date(self):
        return datetime.now().strftime('%x %X')

    def printi(self, log, *args):
        level_debug = 'LOG'
        inline = False
        temp_label = '%s - DEBUG %s: %s'

        for i in args:
            if i == 'inline':
                inline = True
            elif i == 'core':
                level_debug = 'CORE'

        debug = temp_label % (self.get_time(), level_debug, log)
        
        start_time = str(datetime.now().strftime('%x')).replace('/', '-')
        #log = self.replace_words(log, '', '\n', '\r')

        try:
            with open(self.root_path + 'debug/debug-%s.txt' % start_time,'a') as file:
                file.write(str(debug+'\n'))
        except UnicodeEncodeError:
            self.printi('Not a string, mother...', 'core')
            
        #debug_file.close()

        # if inline:
        #     stdout.write(debug + str(' ' * (50 - len(log))) + '\r')
        #     stdout.flush()
        # else:
        print(debug)