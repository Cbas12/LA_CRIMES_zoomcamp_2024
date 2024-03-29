# LA CRIMES MAP AND ANALYSIS
LA CRIMES MAP AND ANALYSIS project repository by Sebastian Peralta for DE Zoomcamp 2024 

**IMPORTANT**

THIS PROJECT WAS CREATED FOR EDUCATIONAL PURPOSES. ALL THE NECESITIES MENTIONED HERE AND MENTIONS OF ANY REAL WORLD ENTITIES NEED TO BE CONSIDERED AS FICTIONAL OR NONE VERIFIED. 

**PROBLEM**

The citizens of Los Angeles need a constantly updated map for all crimes reported in the city. They need to be able to know where exactly each crime was committed and which type. For creating awareness about the situation of cyber crimes, they also require to know the commonality of this set of activities, including information of which exact type was and which are the most targeted groups. For this, a new, free and open dashboard was proposed.

Unfortunatelly, due to security concerns and mandatory regulations, the LAPD won't allow 3rd parties to have direct access to their databases. Luckily, there is a workaround, which is that the LAPD agrees to configure their systems so, once a day, they export all data of new regristred crimes into a Google Drive folder as a Google Sheet.

We need to design a tool that will retrieve this data from the Google Sheet, transform and upload into a comfortable repository from which a dashboard tool can easily pull the information. The proposal was to use MageAi in conjuction with Big Query (GCP) and Google Cloud Storage (GCP). The selected dashboard tool was Power BI. 


**DETAILS OF THE PROJECT**

The LA CRIMES MAP AND ANALYSIS uses the following tools:
- Google Sheets
- Google Sheets API
- Google Cloud Storage (GCP)
- Big Query (GCP)
- Mage
- Power BI

How this works?
1) Data is uploaded to a Google Sheet file
2) Mage reads the data and upload it as two new parquet files in GCS. One is a temporal file that is replaced with each run, the other is placed in a specific folder to serve as historical data
3) Mage pulls the new data from GCS to Big Query
4) Mage reads the new data in Big Query and applies different transformation to with the use of PySpark
5) Mage constrast the new transformed data with the one already found in the main table from which the dashboard pulls all its data
6) Mage inserts the new data into the main table, but only the the rows that belong to a later date than the latest one found in the main table, in order to avoid duplicating information. This is in case there is ever any issue with the updates of the Google Sheet file.
7) The Power BI dashboards connects directly to the data of the main table



**HOW TO RUN THE PROJECT**

Necesary/Helpful files: https://drive.google.com/drive/folders/1A7cKGeQAQyzHwYU1wLqD_9zFuOK69kq9?usp=sharing

**Setting up the enviroment**

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
  b. Inside the bucket upload the file "LA_CRIME_DATA.parquet" which can be find in the Necesary/Helpful files folder provided above. 
  c. Inside the bucket create a folder with the name "historical_data" 
  d. In Big Query create a new dataset "sp_project_bq" 
  e. Create a new query, then modify and run the following commands (change [YOU_PROJECT_ID] to your GCP project id), one by one:
    
    CREATE OR REPLACE EXTERNAL TABLE `[YOU_PROJECT_ID].sp_project_bq.ext_la_crimes_data` OPTIONS ( format = 'parquet', uris = ['gs://sp_project_bucket/LA_CRIME_DATA.parquet']);
    
    CREATE OR REPLACE TABLE `[YOU_PROJECT_ID].sp_project_bq.LA_CRIME_DATA` PARTITION BY DATE_REPORTED AS SELECT * FROM `[YOU_PROJECT_ID].sp_project_bq.ext_la_crimes_data`;
   
  This will create your schema and migrate 2020 to 2023 data. We'll work and test this project with 2024 data.

3) Google Drive and Sheets

  a. Create a folder in Google Drive and upload the file "daily_crimes" located in the Necesary/Helpful files folder provided above. 
  b. Once it's in the folder, open the file and clic on "Share".   
  c. Clic in "Copy link" and you'll get an url similar to this: https://docs.google.com/spreadsheets/d/[random_string_of_characters]/edit?usp=sharing 
  d. We'll save that link for later.


**Building the pipeline**

1) Start MageSpark Container 

  a. Run the command to build the docker image:
  
    docker build -t mage_spark

  b. Run the command to start mage:
  
    docker run -it --name mage_spark -e SPARK_MASTER_HOST='local' -p 6789:6789 -v $(pwd):/home/src mage_spark /app/run_app.sh mage start sp_project_zoomcamp

  Steps a and b are only needed when creating the container, so you only need to run them once.

  c. (Optional) In case you want to pause your work, just run the following commands, one by one:

  Get the container id:
    
    docker ps

  Once you have the id:
    
    docker stop [insert docket id]

  d. (Optional) When you want to resume:
  
    docker start [insert docket id]

2) Adding required files to codespace

  a. Place the api key json file that you generated while setting up your GCP account in the codespace main directory. For security reasons, the .gitignore is configured to not comit any .json files into Github.

  b. Rename the file into "my_gcp_key.json"

3) Making some adjustments to Mage

  a. Enter mage which should be takling port 6789 (127.0.0.1:6789/)

  b. Enter the files tab (http://127.0.0.1:6789/files) and perform the following actions:
    -Open "io_config.yaml" and add/modify the line "GOOGLE_SERVICE_ACC_KEY_FILEPATH:" by adding "my_gcp_key.json" after the ":"

  c. Go to piplines (http://127.0.0.1:6789/pipelines?_limit=30) and access "etl_project_sp"

  d. Enter to "edit pipeline" by navigating the left bar and perform the following actions:
    - In data loader "ext_google_sheets", change the value of the variable "sheet_url" to your own link to your own Google Sheet, which we got in step 3) of Setting up the enviroment.
    - In the transformer "get_data_bq", change the value of the variable "query" by replacing the part that contains "spatial-vision-412003" to your own GCP project id name. Do the same for the variable "query_select".
    - In the data exporter "load_bq", change the values of the variables "table_id" and "query_max_date" by replacing the parts that contains "spatial-vision-412003" to your own GCP project id name.

4) Setting trigger and testing

  a. After making sure we saved all our modifications, we'll go "Triggers" by navigating the left bar 
  b. Clic on "+ New trigger" and select "Schedule". 
  c. Put a name to your trigger, select a the "daily" frecuency and configure the "Start date and time" to tomorrow at 00:10. 
  d. Clic on "Saves changes" 
  f. Enter your newly created trigger and clic on "Enable trigger" before clicing in "Run@once". 
  g. Wait for the pipiline to finish and confirm the "Done" status before going into Big Query and checking the results. The LA_CRIME_DATA table should now have Jan 1 2024 data. 


**OPTIONAL STEPS**
If you wish to make some additional test with other days of data, you just need to open your Google Sheet and paste the data from the file "Crime_Data_2024_fragment.xlsx" which is found in place the Necesary/Helpful files folder. Enter the file and filter any day you want to test before copying and pasting it to the Google Sheet 

## Acknowledgments

I would like to express my gratitude to the following individuals and resources for their invaluable contributions to this project:

1. **DataTalks Club Instructors**:
   - **Ankush Khanna**: For sharing expertise and insights on data engineering.
   - **Victoria Perez Mola**: For her guidance and support throughout the course.
   - **Alexey Grigorev**: For teaching us about workflow orchestration with Mage.
   - **Matt Palmer**: For his valuable input on analytics engineering.
   - **Luis Oliveira**: For insights into batch processing and Spark.
   - **Michael Shoemaker**: For his contributions to the course content.

2. **DataTalks Club Community**:
   - The vibrant community at DataTalks Club provided a supportive environment for learning and collaboration.

3. **Open Source Tools and Platforms**:
   - **PySpark**, **Pandas**, **Mage.ai**, **Power BI**, and **Google Cloud Platform** were instrumental in building this project.

4. **Special Thanks**:
   - Last but not least, heartfelt thanks to the DataTalks Club instructors who helped me develop the skills necessary to create this project.

Without their collective efforts, this project would not have been possible. 🙌🎉