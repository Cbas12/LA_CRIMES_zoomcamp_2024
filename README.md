# DE_Zoomcamp_2024_Project_SPeralta
DE Zoomcamp 2024 Project repository by Sebastian Peralta

Step 1: Run:
docker build -t mage_spark

Step 2: Run:
docker run -it --name mage_spark -e SPARK_MASTER_HOST='local' -p 6789:6789 -v $(pwd):/home/src mage_spark \
  /app/run_app.sh mage start sp_project_zoomcamp

Step 3: Run:
docker start [insert docket id]

Step 4: Run:
docker stop [insert docket id]