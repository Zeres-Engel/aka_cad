from src import Nester, Material, Object

def main():
    material = Material(width=1000, height=1000,)

    nester = Nester()

    nester.add_material(material)
    
    ob1 = Object(img_path='data/obj1.jpg')
    
    nester.add_object(ob1, num_copies=17)
    nester.nest()
    nester.export_map()


if __name__ == "__main__":
    main()
