import rasterio
import numpy as np
from PIL import Image


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


def create_preview(file_path: str, output_path: str):
    with rasterio.open(file_path) as dataset:
        if dataset.count >= 3:
            data = dataset.read([1, 2, 3])

            bands = []

            for band in data:
                low, high = np.percentile(band, (2, 98))

                if high > low:
                    band = np.clip((band - low) / (high - low), 0, 1)
                else:
                    band = np.zeros_like(band, dtype="float32")

                bands.append((band * 255).astype("uint8"))

            image_array = np.stack(bands, axis=-1)

        else:
            band = dataset.read(1)

            low, high = np.percentile(band, (2, 98))

            if high > low:
                band = np.clip((band - low) / (high - low), 0, 1)
            else:
                band = np.zeros_like(band, dtype="float32")

            image_array = (band * 255).astype("uint8")

        image = Image.fromarray(image_array)
        image.thumbnail((1200, 1200))
        image.save(output_path)