# Tutorial
# https://here.isnew.info/how-to-save-a-numpy-array-as-a-geotiff-file-using-gdal.html

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt


def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds


def write_geotiff(filename, arr, in_ds):
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Int32

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(filename, arr.shape[1], arr.shape[0], 1, arr_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.FlushCache()
    band.ComputeStatistics(False)


nlcd01_arr, nlcd01_ds = read_geotiff("nlcd2001_clipped.tif")
nlcd16_arr, nlcd16_ds = read_geotiff("nlcd2016_clipped.tif")

nlcd_changed = np.where(nlcd01_arr != nlcd16_arr, 1, 0)

write_geotiff("nlcd_changed.tif", nlcd_changed, nlcd01_ds)

plt.subplot(311)
plt.imshow(nlcd01_arr)

plt.subplot(312)
plt.imshow(nlcd16_arr)

plt.subplot(313)
plt.imshow(nlcd_changed)

plt.savefig("image.png")
