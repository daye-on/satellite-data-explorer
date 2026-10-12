# datacube

### Desc
위성이미지를 DB에서 metadata를 저장하고, 스토리지에서 관리하고 싶을 때 사용하는 방법.<br>
product: 밴드, 좌표계, 측정값, 구조 등 데이터 셋의 정의
metadata: 실제 관측정보, 시간, 위치, 파일 경로 등 개별 데이터셋의 메타데이터
```text
product.yaml
        │
        │ 정의
        ▼
 Product
        │
        ├──────────────┐
        │              │
metadata1.yaml   metadata2.yaml
        │              │
        ▼              ▼
 Dataset1       Dataset2
```

<br>

### 파일 설명
* main.py : 산출물의 메타데이터를 추출하여 yaml 형태의 파일로 생성하기 위함.

<br>

### 초기 세팅

```bash
nano datacube.conf

[datacube]
db_hostname: localhost
db_port: 5434
db_database: postgres
db_username: postgres
db_password: opendatacubepassword
```

```bash
datacube system init

[output]
Initialising database...
Created.
Checking indexes/views.
Done.
```

<br>

### yaml 형태의 결과물 DB 저장
```bash
datacube product add ./sample/product/chl.odc-product.yaml

[output] Adding "chl_product" (this might take a while) DONE
```
```bash
datacube dataset add ./sample/metadata/UST21_L3_Merged-Chla-1D_20260102.nc.odc-metadata.yaml

[output] Indexing datasets  [####################################]  100%
```

<br>

### 해당 변수의 메소드 확인 - dir( )
```python
import datacube

dc = datacube.Datacube(app="my_analysis")
print(dir(dc))

['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_dask_load', '_list_measurements', '_xr_load', 'close', 'create_storage', 'find_datasets', 'find_datasets_lazy', 'group_datasets', 'index', 'list_measurements', 'list_products', 'load', 'load_data']
```