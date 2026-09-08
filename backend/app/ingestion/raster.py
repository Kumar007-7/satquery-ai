import rasterio


def inspect_raster(file_path: str):
    with rasterio.open(file_path) as dataset:
        return {
            "width": dataset.width,
            "height": dataset.height,
            "bands": dataset.count,
            "crs": str(dataset.crs),
            "dtype": dataset.dtypes[0],
            "bounds": {
                "left": dataset.bounds.left,
                "bottom": dataset.bounds.bottom,
                "right": dataset.bounds.right,
                "top": dataset.bounds.top,
            },
        }