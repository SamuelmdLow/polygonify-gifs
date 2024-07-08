from PIL import Image
import sys
import random
import math

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
                    nextX = stepX*d + o[0]
                    nextY = stepY*d + o[1]
                    if x > 0 and x < self.image.width and y > 0 and y < self.image.height:
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
    #sys.argv[1]
    #im = Image.open(r"C:\Users\tubbd\Pictures\art\theBoys.png")
    poly_num = 5
    edges = 3

    poly = Polygonify(Image.open(r"C:\Users\tubbd\Downloads\checktitle.png"), poly_num, edges)
    p = poly.polygonify()

    print(p)