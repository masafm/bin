#!/usr/bin/env python3
import sys
import yaml
 
def main():
    f = argnum
    print('file: ' + f)
 
    data = yaml.safe_load(open(f).read())
    print(data)
 
if __name__ == "__main__": 
        args = sys.argv
          
        if len(args) == 2:
            argnum = args[1]
            main()
        else:
            print ('Usage: Specify yaml file path.')
            sys.exit()
