import os
path_fd=os.path.dirname(os.path.realpath(__file__))+'/'
os.chdir(path_fd)

import pathlib, uuid, yaml
import netCDF4 as nc

from affine import Affine
from datetime import datetime


class Metadata(object):
    def __init__(self, filename, product_name, product_properties, measurements_name_list, crs):
        self.ds = nc.Dataset(f'{filename}')
        self.metadata_name = '/' + filename.split('/')[-1] + '.odc-metadata.yaml'

        self.dataset_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f'{filename}'))
        self.product_name = product_name
        self.product_properties = product_properties
        self.measurements_name_list = measurements_name_list
        self.crs = crs
        self.filename = filename.split('/')[-1]
        self.generated_path = './sample/metadata'
        
    # Calculate affine transform from coordinates
    def calculate_transform(self, lon, lat):
        lon_diff = lon[1] - lon[0]
        lat_diff = lat[1] - lat[0]

        transform = Affine.translation(lon[0], lat[0]) * Affine.scale(lon_diff, lat_diff)
        return [float(transform.a), float(transform.b), float(transform.c),
                float(transform.d), float(transform.e), float(transform.f),
                float(transform.g), float(transform.h), float(transform.i)]

    def generate_odc_metadata(self):
        lon = self.ds.variables['lon'][:].data.reshape(-1)
        lat = self.ds.variables['lat'][:].data.reshape(-1)
        transform = self.calculate_transform(lon, lat)

        properties = {}
        properties_dict = self.product_properties
        if properties_dict:
            for key, values in properties_dict.items():
                properties[key] = values

        properties_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        properties_time_dict = {
            'datetime': properties_time,
            'odc:processing_datetime': properties_time
        }
        properties.update(properties_time_dict)

        # minio_nc_filename = f'https://dl.s-dev.ust21.kr/tz-bucket/chl/{self.filename}'
        minio_nc_filename = f'https://example.com/{self.filename}'
        measurements = {}
        for name in self.measurements_name_list:
            measurements[name] = {
                'path': minio_nc_filename
            }

        odc_metadata = {
            'id': self.dataset_id,
            '$schema': 'https://schemas.opendatacube.org/dataset',
            'product': {'name': self.product_name},
            'crs': f'EPSG:{self.crs}',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [float(lon.min()), float(lat.min())],
                        [float(lon.max()), float(lat.min())],
                        [float(lon.max()), float(lat.max())],
                        [float(lon.min()), float(lat.max())],
                        [float(lon.min()), float(lat.min())]
                    ]
                ]
            },
            'grids': {
                'default': {
                    'shape': [len(lat), len(lon)],
                    'transform': transform
                }
            },
            'measurements': measurements,
            'properties': properties,
            'lineage': {}
        }

        with open(os.path.join(self.generated_path + self.metadata_name), 'w') as f:
            yaml.dump(odc_metadata, f, default_flow_style=False, allow_unicode=True)
        print(yaml.dump(odc_metadata, default_flow_style=False))