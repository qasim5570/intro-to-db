rm -rf backend frontend

mkdir -p app/pages
mkdir -p app/db
mkdir -p app/services
mkdir -p app/models
mkdir -p app/utils
mkdir -p scripts
mkdir -p docs/report

touch app/Home.py
touch app/pages/1_Browse_Events.py
touch app/pages/2_Event_Details.py
touch app/pages/3_My_Plans.py
touch app/pages/4_Admin_Data_Refresh.py
touch app/db/postgres.py
touch app/db/mongo.py
touch app/services/eventbrite_client.py
touch app/services/openweather_client.py
touch app/services/data_sync.py
touch app/models/__init__.py
touch app/utils/__init__.py
touch scripts/seed_data.py
touch requirements.txt
touch .env

echo "Streamlit-only structure created successfully."
