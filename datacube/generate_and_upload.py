import os
from affine import Affine
from datetime import datetime
import netCDF4 as nc
import minio
import pathlib
import uuid
import yaml

    # try:
    #     f = open('./value.txt','r')
    # except FileNotFoundError:
    #     f = open('datacube/value.txt', 'r')


class NetCDF(object):
    def __init__(self, filename, product_name, product_properties, measurements_name_list, crs):
        print(f"init,")
        self.ds = nc.Dataset(f'{filename}')
        self.metadata_name = '/' + filename.split('/')[-1] + '.odc-metadata.yaml'

        self.dataset_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f'{filename}'))
        self.product_name = product_name
        self.product_properties = product_properties
        self.measurements_name_list = measurements_name_list
        self.crs = crs

        self.generated_path = os.path.join('datacube/generated')
        if self.generated_path:
            pathlib.Path(self.generated_path).mkdir(parents=True, exist_ok=True)

        # minio setting
        minio_end_point = '192.168.101.111:9000'
        minio_original_bucket_name = 'open-data-cube'
        minio_process_bucket_name = 'open-data-cube-process'
        minio_path = 'nosc-data/khoa-chl'
        self.minio_original_path_url = f'http://{minio_end_point}/{minio_original_bucket_name}/{minio_path}{self.metadata_name}'
        self.minio_process_path_url = f'http://{minio_end_point}/{minio_process_bucket_name}/{minio_path}{self.metadata_name}'

        global client
        client = minio.Minio(
            minio_end_point,
            access_key="UOR2rXPi8IeozW3DA8fY",
            secret_key="r9jcVhqXMBS3CoV9ubff6E2lmTjysKiZrMcOF7yJ",
            secure=False
        )

        if not client.bucket_exists(minio_process_bucket_name):
            raise Exception(f'"{minio_process_bucket_name}" Bucket does not exists')


    # Calculate affine transform from coordinates
    def calculate_transform(self, lon, lat):
        print(f"transform,")

        lon_diff = lon[1] - lon[0]
        lat_diff = lat[1] - lat[0]

        transform = Affine.translation(lon[0], lat[0]) * Affine.scale(lon_diff, lat_diff)
        return [float(transform.a), float(transform.b), float(transform.c),
                float(transform.d), float(transform.e), float(transform.f),
                float(transform.g), float(transform.h), float(transform.i)]

    def generate_odc_metadata(self):
        if os.path.isfile(os.path.join(self.generated_path + self.metadata_name)) == True:
            print(f'Already Exist file - {self.generated_path + self.metadata_name}')
        else:
            print(f'generate,')

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

            minio_nc_filename = self.minio_original_path_url.replace('.odc-metadata.yaml','')
            measurements = {}
            for name in self.measurements_name_list:
                measurements[name] = {
                    'path': minio_nc_filename
                }

            odc_metadata = {
                'id': self.dataset_id,
                '$schema': 'https://schemas.opendatacube.org/dataset',
                'location': minio_nc_filename + '.stac-item.json',
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

            # print(yaml.dump(odc_metadata, default_flow_style=False))
            with open(os.path.join(self.generated_path + self.metadata_name), 'w') as f:
                yaml.dump(odc_metadata, f, default_flow_style=False, allow_unicode=True)

        result = f"{self.generated_path + self.metadata_name}"
        return result
