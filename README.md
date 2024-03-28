# LA CRIMES MAP AND ANALYSIS
LA CRIMES MAP AND ANALYSIS project repository by Sebastian Peralta for DE Zoomcamp 2024

HOW TO RUN THE PROJECT

Setting up the enviroment

1) Github Codespace
This project is thought to be used with a Github Codespace, which you can learn how to set up in video DE Zoomcamp 1.4.2 - Using Github Codespaces for the Course (by Luis Oliveira):
https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15

2) GCP
For this project you'll requiere a GCP account as we'll be using Big Query, Google Cloud Storage and Google Sheets API
You can learn how to set up your GCP account and access Google Cloud Storage and Big Query in video DE Zoomcamp 1.1.1 - Introduction to Google Cloud Platform: https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4
Make sure to save your api key json file, as you will need it later
Afterwards go to configure the Google Sheets API for your account in the following link: https://console.cloud.google.com/apis/library/sheets.googleapis.com
Now that you have all that complete the following actions:
  a. In GCS create a new bucket with the name "sp_project_bucket"
  b. Inside the bucket upload the file "LA_CRIME_DATA.parquet" which can be find in: https://drive.google.com/drive/folders/1A7cKGeQAQyzHwYU1wLqD_9zFuOK69kq9?usp=sharing
  c. Inside the bucket create a folder with the name "historical_data"
  d. In Big Query create a new dataset "sp_project_bq"
  e. Create a new query and run the following commands, one by one:
    
    CREATE OR REPLACE EXTERNAL TABLE `[YOU_PROJECT_ID].sp_project_bq.ext_la_crimes_data` OPTIONS ( format = 'parquet', uris = ['gs://sp_project_bucket/LA_CRIME_DATA.parquet']);
    
    CREATE OR REPLACE TABLE `spatial-vision-412003.sp_project_bq.LA_CRIME_DATA` PARTITION BY DATE_REPORTED AS SELECT * FROM `spatial-vision-412003.sp_project_bq.ext_la_crimes_data`;
   
  This will create your schema and migrate 2023 data. We'll work and test this project with 2024 data.


Building the pipeline

1) Start MageSpark Container

  a. Run the command to build the docker image:
    docker build -t mage_spark

  b. Run the command to start mage:
    docker run -it --name mage_spark -e SPARK_MASTER_HOST='local' -p 6789:6789 -v $(pwd):/home/src mage_spark /app/run_app.sh mage start sp_project_zoomcamp

  c. (Optional) In case you want to pause your work, just run the following commands, one by one:

    Get the container id:
      docker ps

    Once you have the id:
      docker stop [insert docket id]

  d. (Optional) When you want to resume:
    docker start [insert docket id]

2) Making some adjustments to Mage


3) Testing