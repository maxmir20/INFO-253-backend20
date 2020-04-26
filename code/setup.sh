docker network create my-network

docker run --name mongo -p 27017:27017 --network my-network -dit mongo:latest

docker build -t add_gsheet_data_to_mongo_image .

docker run -dit --name add_gsheet_data_to_mongo  --network my-network add_gsheet_data_to_mongo_image

cd app/

docker build -t link_api_image .

docker run  -dit --name=link_api -e FLASK_APP=app.py -p 5000:5000 --network my-network link_api_image