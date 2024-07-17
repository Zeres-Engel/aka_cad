from src import Nester, Object, Material
import numpy as np
from utils import export_nest_map, export_raw_svg

def main():
    nester = Nester()
    print("Setting materials...")
    nester.add_material(Material(width=1000, height=1000))
    nester.add_material(Material(width=200, height=200))

    print("Adding objects...")
    
    nester.add_object(Object(img_path='/app/aka_cad/data/objects/obj1.svg'), num_copies=4)
    nester.add_object(Object(img_path='/app/aka_cad/data/objects/obj2.svg'), num_copies=5)
    nester.add_object(Object(img_path='/app/aka_cad/data/objects/obj3.svg'), num_copies=3)
    
    print("Nesting objects...")
    nester.nest()
    nester.export_map()
    nester.export_svg()

if __name__ == "__main__":
    main()
