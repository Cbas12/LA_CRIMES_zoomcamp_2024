# LA CRIMES MAP AND ANALYSIS DASHBOARD PROJECT
Welcome to the LA Crimes Map and Analysis project repository, created by Sebastian Peralta for the Data Engineering Zoomcamp 2024, organized by the DataTalks Club community. In this project, we explore crimes commited in Los Angeles, aiming to create awareness and insights through data visualization and analysis.

## Disclaimer

This crime dashboard is a project created for educational purposes. The data used in this dashboard is sourced from publicly available dataset and I can't confirm if its reflects real-time or official crime statistics. For more information refer to the [Crime Data from 2020 to Present page in Data.gov](https://catalog.data.gov/dataset/crime-data-from-2020-to-present). The problem described here is purely fictional. The citizens of Los Angeles do not currently have access to this specific dashboard nor the LAPD is uploading its crime registers to a Google Sheet file.


## Contact

Any doubts or concerns about running the program please contact me through the next email: sebastianperalta@hotmail.com


## Problem to solve

The citizens of Los Angeles need a constantly updated map for all crimes reported in the city. They need to be able to know where exactly each crime was committed and which type. For creating awareness about the situation of cyber crimes, they also require to know the commonality of this set of activities, including information of which exact type was and which are the most targeted groups. For this, a new, free and open dashboard was proposed.

Unfortunatelly, due to security concerns and mandatory regulations, the LAPD won't allow 3rd parties to have direct access to their databases. Luckily, there is a workaround, which is that the LAPD agrees to configure their systems so, once a day, they export all data of new regristred crimes into a Google Drive folder as a Google Sheet.

We need to design a tool that will retrieve this data from the Google Sheet, transform and upload into a comfortable repository from which a dashboard tool can easily pull the information. The proposal was to use MageAi in conjuction with Big Query (GCP) and Google Cloud Storage (GCP). The selected dashboard tool was Power BI. 


## Details of the project

**The LA CRIMES MAP AND ANALYSIS DASHBOARD project uses the following tools:**
- Google Sheets
- Google Sheets API
- Google Cloud Storage (GCP)
- Big Query (GCP)
- Mage
- Power BI

**How this works?**
1) Data is uploaded to a Google Sheet file
2) Mage reads the data and upload it as two new parquet files in GCS. One is a temporal file that is replaced with each run, the other is placed in a specific folder to serve as historical data
3) Mage pulls the new data from GCS to Big Query
4) Mage reads the new data in Big Query and applies different transformation to with the use of PySpark
5) Mage constrast the new transformed data with the one already found in the main table from which the dashboard pulls all its data
6) Mage inserts the new data into the main table, but only the the rows that belong to a later date than the latest one found in the main table, in order to avoid duplicating information. This is in case there is ever any issue with the updates of the Google Sheet file.
7) The Power BI dashboards connects directly to the data of the main table

**Final result: [Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYWUxMDJiZWItZjdjMi00YTYxLTlmYWYtYmFkYzIwZmE3YmYxIiwidCI6IjBlMGNiMDYwLTA5YWQtNDlmNS1hMDA1LTY4YjliNDlhYTFmNiIsImMiOjR9)**

## Setting up the enviroment

[*Necesary/Helpful files*](https://drive.google.com/drive/folders/1A7cKGeQAQyzHwYU1wLqD_9zFuOK69kq9?usp=sharing)

1. Github Codespace<br>
This project is thought to be used with a Github Codespace, which you can learn how to set up in video D[E Zoomcamp 1.4.2 - Using Github Codespaces for the Course (by Luis Oliveira)](https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15)

2. GCP<br>
  For this project you'll requiere a GCP account as we'll be using Big Query, Google Cloud Storage and Google Sheets API. You can learn how to set up your GCP account and access Google Cloud Storage and Big Query in video [DE Zoomcamp 1.1.1 - Introduction to Google Cloud Platform](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4). Make sure to save your api key json file, as you will need it later. Afterwards go to configure the Google Sheets API for your account by clicking this [link](https://console.cloud.google.com/apis/library/sheets.googleapis.com). Afterwards, complete the following actions:
    - In GCS create a new bucket with the name "sp_project_bucket"
    - Inside the bucket upload the file "LA_CRIME_DATA.parquet" which can be find in the Necesary/Helpful files folder provided above.
    - Inside the bucket create a folder with the name "historical_data"
    - In Big Query create a new dataset "sp_project_bq"
    - Create a new query, then modify and run the following commands (change [YOU_PROJECT_ID] to your GCP project id), one by one:
    ```
    CREATE OR REPLACE EXTERNAL TABLE `[YOU_PROJECT_ID].sp_project_bq.ext_la_crimes_data` 
    OPTIONS ( format = 'parquet', uris = ['gs://sp_project_bucket/LA_CRIME_DATA.parquet']);
    ```
    ```
    CREATE OR REPLACE TABLE `[YOU_PROJECT_ID].sp_project_bq.LA_CRIME_DATA` 
    PARTITION BY DATE_REPORTED AS SELECT * FROM `[YOU_PROJECT_ID].sp_project_bq.ext_la_crimes_data`;
    ```
    - This will create your schema and migrate 2020 to 2023 data. We'll work and test this project with 2024 data.

3. Google Drive and Sheets:
    1. Create a folder in Google Drive and upload the file "daily_crimes" located in the *Necessary/Helpful files* folder provided above.
    2. Once it's in the folder, open the file and click on "Share."
    3. Click on "Copy link," and you'll get a URL similar to this: `https://docs.google.com/spreadsheets/d/[random_string_of_characters]/edit?usp=sharing`.
    4. We'll save that link for later.


## Building the pipeline

**Start MageSpark Container**<br>
1. Run the command to build the docker image:  
  `docker build -t mage_spark .`
2. Run the command to start mage (Steps a and b are only needed when creating the container, so you only need to run them once):
  `docker run -it --name mage_spark -e SPARK_MASTER_HOST='local' -p 6789:6789 -v $(pwd):/home/src mage_spark /app/run_app.sh mage start sp_project_zoomcamp`
3. (Optional) In case you want to pause your work, just Ctrl + C.
4. (Optional) When you want to resume your work run the following commands, one by one:
    - Get the container id:<br>
  `docker ps`
    - Once you have the id:<br>
  `docker start [insert docket id]`
5. (Optional) When you want to stop again:<br>
  `docker stop [insert docket id]`<br>

**Adding required files to codespace**<br>
1. Place the api key json file that you generated while setting up your GCP account in the codespace main directory. For security reasons, the .gitignore is configured to not comit any .json files into Github.
2. Rename the file into "my_gcp_api_key.json"<br>

**Making some adjustments to Mage**<br>
1. Enter mage which should be taking port 6789. You'll find the link in the "Ports" section of your codespace.
2. After mage loads, enter the piplines tab and access "etl_project_sp"
3. To edit the pipeline, follow these steps:
    - Enter the "Edit pipeline" tab
    - In the data loader component "ext_google_sheets", update the value of the variable "sheet_url" with your own link to your Google Sheet (as obtained in step 3 of setting up the environment).
    - In the transformer component "get_data_bq", replace the value of the variable "gcp_project" with the name of your own GCP project ID name.
    - In the data exporter component "load_bq", do the same as the previous step, replace the value of the variable "gcp_project" with the name of your own GCP project ID name.<br>

**Setting trigger and testing**<br>
1. After making sure we saved all our modifications, we'll go "Triggers" by navigating the left bar 
2. Clic on "+ New trigger" and select "Schedule". 
3. Put a name to your trigger, select a the "custom" frecuency.
4. In "Cron expression" place the next syntax: `10 0 * * *`. This will configure the pipeline to run every day at 00:10.
5. Clic on "Saves changes" 
6. Enter your newly created trigger and clic on "Enable trigger" before clicing in "Run@once". 
7. Wait for the pipiline to finish and confirm the "Done" status before going into Big Query and checking the results. The LA_CRIME_DATA table should now have Jan 1 2024 data.<br>

**OPTIONAL STEPS**
<br>If you wish to make some additional tests with other days of data, you just need to open your Google Sheet and paste the data from the file "Crime_Data_2024_fragment.xlsx" which is found in place the Necesary/Helpful files folder. Enter the file and filter any day you want to test before copying and pasting it to the Google Sheet. You can also test the triggers by changing the cron expression to different times.

## Acknowledgments

I would like to express my gratitude to the following individuals and resources for their invaluable contributions to this project:

1. **DataTalks Club Instructors**:
   - Ankush Khanna
   - Victoria Perez Mola
   - Alexey Grigorev
   - Matt Palmer
   - Luis Oliveira
   - Michael Shoemaker

2. **DataTalks Club Community**:
   - The vibrant community at DataTalks Club provided a supportive environment for learning and collaboration.

3. **Open Source Tools and Platforms**:
   - **PySpark**, **Pandas**, **Mage.ai**, **Power BI**, **Google Sheets** and **Google Cloud Platform** were instrumental in building this project.

4. **Special Thanks**:
   - Last but not least, heartfelt thanks to Matt Palmer and Alexey Grigorev, who helped me learn develop the skills necessary to create this project. Matt allowed to discover Mage, a tool that I found to be very reliable and easy to use. Alexey increased my interest and desire to work with Spark.

Without their collective efforts, this project would not have been possible. 🙌🎉
