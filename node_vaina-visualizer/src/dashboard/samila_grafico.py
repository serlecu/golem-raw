#https://www.samila.site/
#https://www.kaggle.com/code/nulldata/create-generative-art-in-python/notebook
#https://github.com/sepandhaghighi/samila
#https://www.youtube.com/watch?v=pgv0LQBSwJE 
#https://www.theclickreader.com/generating-mathematical-artwork-for-nfts-through-samila-and-python/

import samila
import random
import math
import matplotlib.pyplot as plt
from samila import GenerativeImage, Projection

def crearImagen1frame():
        def f1(x, y):
                result = random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)
                return result
        def f2(x, y):
                result = random.uniform(-1,1) * y**2 - math.cos(x**2) + 2*x
                return result

        g = GenerativeImage(f1, f2)
        g.generate()
        g.plot(color = "white", bgcolor= "black",projection=Projection.AITOFF)
        g.plot(marker="o", spot_size=50)
        g.seed
       # plt.show()
       # plt.close()
        g.save_image(file_adr="test.png", depth=0.7)
        