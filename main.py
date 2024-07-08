from PIL import Image
import sys
import random
import math
import json

class Polygonify:
    def __init__(self, image, poly_num, edge_count):
        self.image = image
        self.px = image.load()
        self.poly_num = poly_num
        self.edge_count = edge_count
        self.origins = []

    def verifyPixel(self, pixel):

        return pixel[0] > 100

    def plant(self):

        self.origins = []

        for i in range(self.poly_num):
            trys = 0
            while trys < (self.image.width * self.image.height)/2:
                x = random.randint(0, self.image.width - 1)
                y = random.randint(0, self.image.height - 1)
                if self.verifyPixel(self.px[x, y]):
                    self.origins.append((x,y))
                    break
                else:
                    trys = trys + 1

        return self.origins

    def grow(self):

        polygons = []

        deg = ((2*math.pi)/self.edge_count)
        for i in range(len(self.origins)):
            o = self.origins[i]

            polygons.append(
                {'origin': o,
                 'edges': []}
            )

            #print("polygon #%i", i)

            for e in range(self.edge_count):
                #print("edge #%i", e)
                x = o[0]
                y = o[1]
                stepX = math.cos(e * deg)
                stepY = math.sin(e * deg)
                d = 0
                while self.verifyPixel(self.px[x,y]):
                    #print("d #%i", d)
                    nextX = math.floor(stepX*d + o[0])
                    nextY = math.floor(stepY*d + o[1])
                    if nextX > 0 and nextX < self.image.width and nextY > 0 and nextY < self.image.height:
                        if self.verifyPixel(self.px[nextX, nextY]):
                            x = nextX
                            y = nextY
                            d = d + 1
                            continue

                    polygons[-1]['edges'].append((x,y))
                    break

        return polygons


    def polygonify(self):
        self.plant()
        p = self.grow()
        return p

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\npython main.py input_file output_file edge_count polygon_number\n")
    else:
        
        char_arg = [False, False]
        int_arg = [False, False]
        poly_num = 5
        edges = 3

        for a in sys.argv[1:]:
            if a.isnumeric():
                for i in range(len(int_arg)):
                    if not int_arg[i]:
                        int_arg[i] = int(a)
                        break
            else:
                for i in range(len(char_arg)):
                    if not char_arg[i]:
                        char_arg[i] = a
                        break

        if char_arg[0]:
            input_file = char_arg[0]
            if int_arg[0]:
                poly_num = int_arg[0]
            if int_arg[1]:
                edges = int_arg[1]
            
            poly = Polygonify(Image.open(r""+input_file), poly_num, edges)
            p = poly.polygonify()

            if not char_arg[1]:
                print(p)
            else:
                output_file = char_arg[1]
                json_object = json.dumps(p, indent=4)
 
                with open(output_file, "w") as outfile:
                    outfile.write(json_object)
                print("\nWritten to '" + output_file + "' successfully!\n")
        else:
            print("You must have an argument to an input file")