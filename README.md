# Tutorial Installasi 

Sebelum mengunduh / melakukan **cloning** repositori ini, pastikan branch Fachry yang dipilih.

1. Unduh datasource pada dataset-olist_task1/helper/source_init/init.sql atau https://github.com/Kurikulum-Sekolah-Pacmann/dataset-olist/tree/main/helper/source_init dan import pada DBMS.

2. Buat schema stg dan tabel-tabel yang berhubungan (sebagai tampungan sementara data sebelum diolah ke schema final) dan schema final beserta tabel-tabel yang berhubungan. Kedua kueri dapat diakses pada folder dwh_init. 

3. Buat akun sentry untuk mendapatkan sentry DSN. Link dapat diakses [disini](https://personal-mkf.sentry.io/auth/login/personal-mkf/)

4. Inisialisasi file .env dengan format sebagai berikut : 

```
# Source
SRC_POSTGRES_DB=olist-src
SRC_POSTGRES_HOST=localhost
SRC_POSTGRES_USER=postgres
SRC_POSTGRES_PASSWORD=[SRC_PASSWORD]
SRC_POSTGRES_PORT=[SRC_PORT]

# DWH
DWH_POSTGRES_DB=olist-dwh
DWH_POSTGRES_HOST=localhost
DWH_POSTGRES_USER=postgres
DWH_POSTGRES_PASSWORD=[DWH_PASSWORD]
DWH_POSTGRES_PORT=[DWH_PORT]

# SENTRY DSN
SENTRY_DSN=[SENTRY_DSN_KEY]

DIR_ROOT_PROJECT=<project_dir>
DIR_TEMP_LOG=<project_dir>/pipeline/temp/log         
DIR_TEMP_DATA=<project_dir>/pipeline/temp/data  
DIR_EXTRACT_QUERY=<project_dir>/pipeline/src_query/extract 
DIR_LOAD_QUERY=<project_dir>/pipeline/src_query/load    
DIR_TRANSFORM_QUERY=<project_dir>/pipeline/src_query/transform     
DIR_LOG=<project_dir>/logs/                                    

```

5. Jalankan perintah : 

```
docker-compose up -d
```

6. Lakukan installasi library yang diperlukan dengan menjalankan perintah berikut (pada cmd) : 

```
pip install -r requirements.txt
```

7. Untuk melakukan proses ELT. Hapus terlebih dahulu data pada folder pipeline/temp/data dan pipeline/temp/log. Kemudian jalankan perintah berikut pada cmd :

```
pip install -r requirements.txt
```

> catatan : repositori ini diambil dari https://github.com/Kurikulum-Sekolah-Pacmann/dataset-olist dan dimodifikasi sesuai kebutuhan.