import rasterio
from rasterio.features import sieve
import numpy
import os

wd =r'/media/sf_compartidavm/comprimidas/'
salida = r'/media/sf_compartidavm/comprimidas/mascaras/'
for f in os.listdir(wd):
    if f.endswith(".tif"):
        with rasterio.open(wd + f) as src:
            b1, b2, b3 = src.read()

            profile = src.profile
            profile.update(
                # dtype=rasterio.float32,
                dtype=rasterio.uint8,
                count=1,
                compress='lzw',
                nodata=0)

        red_index = numpy.zeros(b1.shape)
        red_index = (b1.astype(float) - b2.astype(float)) / (b1.astype(float) + b2.astype(float))
        mascara_rojo = numpy.zeros(b1.shape)
        mascara_rojo = (red_index > 0.2) * 1 & (red_index < 0.7) * 1 & (b1 > 60) * 1
        mascara_rojo = sieve(mascara_rojo.astype(rasterio.uint8), size = 400, connectivity = 8)

        # with rasterio.open('red_index.tif', 'w', **profile) as dst:
        #    dst.write(red_index.astype(rasterio.float32), 1)

        with rasterio.open('{0}{1}_mascara.tif'.format(salida, os.path.splitext(f)[0]), 'w', **profile) as dst:
            dst.nodata = 0
            dst.write(mascara_rojo.astype(rasterio.uint8), 1)
    else:
        pass