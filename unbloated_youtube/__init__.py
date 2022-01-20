import sys
import os


librarypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, librarypath)
sys.path.insert(1, os.path.join(librarypath, "backend")) 
sys.path.insert(1, os.path.join(librarypath, "frontend")) 

