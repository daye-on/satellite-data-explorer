# satellite-data-explorer
JupyterHub 환경에서 Datacube를 활용한 위성 데이터 조회, 시각화 및 메타데이터 검증

<br/>

* Jupyterhub
* postgresql
* nativeauthenticator
* opendatacube

<br>

<img width="1920" height="1032" alt="Image" src="https://github.com/user-attachments/assets/ce0da7b7-2c2f-48ab-b138-056c84bd2bde" />
<img width="1920" height="1032" alt="Image" src="https://github.com/user-attachments/assets/8028bf6c-5929-482b-afed-b3c25fc77be7" />
<img width="1920" height="1032" alt="Image" src="https://github.com/user-attachments/assets/465083af-5ac7-42ee-b7c1-9ec44c4c8e01" />

<br/><br/>

### Init
```
git clone <this_repo>
cd Cube
git clone https://github.com/jupyterhub/nativeauthenticator.git

docker compose build
docker compose up -d
docker compose exec jupyterhub datacube -v system init
docker compose exec jupyterhub datacube product add https://raw.githubusercontent.com/digitalearthafrica/config/master/products/esa_s2_l2a.odc-product.yaml

docker cp odc-stac.ipynb jupyterhub:/home/admin
docker cp ./datacube/ jupyterhub:/home/admin
```

<br/>

### Usage
1. http://localhost:8000 접속
2. id가 'admin'인 계정으로 회원가입 후 로그인
3. admin 계정에서 사용자 회원가입 관리 : http://localhost:8000/hub/authorize

<br/>

### Test
```
# test.ipynb
import datacube
dc = datacube.Datacube(app="test")
products = dc.list_products()
products
```
```
# datacube.conf
[datacube]
db_hostname: postgres
db_database: postgres
db_username: postgres
db_password: opendatacubepassword
```

<br/>

### Database
* URL : jdbc:postgresql://localhost:5434/postgres
* Password : opendatacubepassword
* OpenDatacbue Schema : agdc

<br/>

### Error
* Database IDE에서 schema가 'public'만 보인다면, 설정에서 schema 체크를 해줘야 됨.

* `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "postgres" (172.18.0.2), port 5434 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?`
<br/>docker compose 파일에서 jupyterhub DB_PORT 잘못 기입<br/>
* `OperationalError: (psycopg2.OperationalError) connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
	Is the server running locally and accepting connections on that socket?` 
<br/> datacube.conf 파일이 없는 경우<br/>

<br/>

### Ref
* Nativeauthenticator<br/>
    https://hatarilabs.com/ih-en/how-to-set-a-multiuser-jupyterlab-server-with-jupyterhub-in-windows-with-docker

* jupyterhub에서 제공하는 compose 파일을 사용하지 않은 이유<br/>
    사용자 새로 생성할 때마다 사용자 각각의 도커 컨테이너가 추가됨<br/>
    https://github.com/jupyterhub/jupyterhub-deploy-docker

<br/>
