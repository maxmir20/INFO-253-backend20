docker stop link_api
docker stop mongo
docker rm link_api
docker rm mongo
docker rm add_gsheet_data_to_mongo
docker rmi add_gsheet_data_to_mongo_image
docker rmi link_api_image
docker network rm my-network