import datacube
from generate_odc_metadata import Metadata
# from generate_and_upload import NetCDF # minio 세팅 후에 진행할 것

if __name__ == '__main__':
    dc = datacube.Datacube(app="my_analysis")
    product_name = 'chl_product'
    metadata_nc = './sample/UST21_L3_Merged-Chla-1D_20260102.nc'
    prd_info = {}

    try:
        prd_info = dc.index.products.get_by_name(product_name).definition
    except AttributeError as e:
        print('No product')
        sys.exit()
        
    metadata = prd_info.get('metadata')
    measurements = prd_info.get('measurements')
    
    product_properties = {}
    if len(metadata) > 1:
        product_properties = metadata['properties']
        
    measurements_name_list = []
    if len(measurements):
        for m in measurements:
            measurements_name_list.append(m['name'])

    result = Metadata(metadata_nc, product_name, product_properties, measurements_name_list, '4326').generate_odc_metadata()
    # result = NetCDF(file, product_name, product_properties, measurements_name_list, '4326').generate_odc_metadata()
    print('finish')