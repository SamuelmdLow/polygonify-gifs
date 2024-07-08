from PIL import Image
import sys
import random
import math
import json

class Polygonify:
    def __init__(self, image, poly_num, edge_count, percent=False, plantStyle="even"):
        self.image = image
        self.px = image.load()
        self.poly_num = poly_num
        self.edge_count = edge_count
        self.origins = []
        self.percent = percent
        self.plantStyle = plantStyle

    def verifyPixel(self, pixel):
        return pixel[0] < 100

    def plant(self):

        self.origins = []

        if self.plantStyle=="isometric":
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

        elif self.plantStyle=="even":
            tiles = self.getTiles([], self.image.width, self.image.height, math.floor(math.log(self.poly_num, 2)))
            for i in range(self.poly_num):
                t = len(tiles) - 1
                planted = False
                while(t > 0):
                    trys = 0
                    tile_cols = math.floor(self.image.width/tiles[t]['width'])
                    tile_count = tile_cols * (self.image.height / tiles[t]['height'])
                    cutoff = (tiles[t]['width'] * tiles[t]['height'])/10
                    
                    minX = ((i%tile_count) % tile_cols)
                    minY = ((i%tile_count) // tile_cols)
                    #print("minx:%d miny:%d" % (minX, minY))

                    #print("iw:%d ih:%d cols:%d count:%d w:%d h:%d" % (self.image.width, self.image.height, tile_cols, tile_count, tiles[t]['width'],tiles[t]['height']))

                    while trys < cutoff:
                        x = random.randint(minX * tiles[t]['width'], ((minX + 1)  * tiles[t]['width']) - 1)
                        y = random.randint(minY * tiles[t]['height'], ((minY + 1) * tiles[t]['height']) - 1)
                        #print("x:%d y:%d" % (x, y))
                        if self.verifyPixel(self.px[x, y]):
                            self.origins.append((x,y))
                            planted = True
                            break
                        else:
                            trys = trys + 1
                    
                    if planted == False:
                        t = t - 1
                    else:
                        break

        return self.origins
    
    def getTiles(self, tiles, w, h, n):
        if n < 0 or w < 2 or h < 2:
            return tiles
        else:
            tiles.append({
                'iteration': n,
                'width': w,
                'height': h
            })
            #print('w:%d h:%d' % (w,h))

            if w > h:
                w = math.floor(w/2)
            else:
                h = math.floor(h/2)

        n = n - 1
        return self.getTiles(tiles, w, h, n)


    def grow(self):

        polygons = []

        deg = ((2*math.pi)/self.edge_count)
        for i in range(len(self.origins)):
            o = self.origins[i]

            if (self.percent) :
                polygons.append({
                    'origin': (o[0]/self.image.width, o[1]/self.image.height),
                    'edges': []
                })
            else:
                polygons.append({
                    'origin': o,
                    'edges': []
                })

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

                    if (self.percent) :
                        polygons[-1]['edges'].append((x/self.image.width,y/self.image.height))
                    else:
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
        percent = False

        for a in sys.argv[1:]:
            if a.isnumeric():
                for i in range(len(int_arg)):
                    if not int_arg[i]:
                        int_arg[i] = int(a)
                        break
            else:
                if a == "percent":
                    percent = True
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
            
            poly = Polygonify(Image.open(r""+input_file), poly_num, edges, percent=percent)

            out = {'width': poly.image.width,
                   'height': poly.image.height,
                   'polygons': []
            }
            out['polygons'] = poly.polygonify()

            if not char_arg[1]:
                print(out)
            else:
                output_file = char_arg[1]
                json_object = json.dumps(out, indent=4)
 
                with open(output_file, "w") as outfile:
                    outfile.write(json_object)
                print("\nWritten to '" + output_file + "' successfully!\n")
        else:
            print("You must have an argument to an input file")