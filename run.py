# coding:utf-8
import sys, os, kernel

def get_modules():
    names = [ f[:-3] for f in os.listdir('animals') 
                if f.endswith('.py') and f != '__init__.py']
    modules = [ __import__('animals.%s' % (name,), None, None, ['animals']) 
                for name in names ]
    return modules

def main():
    engine = kernel.engine

    if len(sys.argv)>1 and sys.argv[1] == '-q':
        engine.init_logs() # no pygame interface and use log file instead.
    else:
        engine.init_pygame((800,600))

    for m in get_modules():
        engine.add_lifes( m.make_animals() )

    engine.run()

if __name__ == '__main__':
    main()
