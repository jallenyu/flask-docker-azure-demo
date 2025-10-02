# Flask Docker Azure Deployment
This is a demo for deploying Flask container on Azure.

## Build the Flask Image with Docker

`docker build -t my-flask-app .`

Run locally to see if the container works.

## Hosting Flask Image
Pushing to ACR doesn't work at the moment, because I was unable to create a resource group within the **CoC - Production** subscription, so I created another subscription.

1. Login to ACR

`az login`

`az acr login --name myregistry`

2. Get login server and tag the image

`az acr show --name myregistry --query loginServer --output tsv` , example return: `flaskdockerdemoacr.azurecr.io`

`docker tag my-flask-app flaskdockerdemoacr.azurecr.io/my-flask-app:latest`

3. Push image to ACR

`docker push flaskdockerdemoacr.azurecr.io/my-flask-app:latest`

## Deploy Flask Image to Azure App Service
1. Go to Azure portal, navigate to App Service
2. Create a resource
3. Web app
4. Choose the right registry, input the image name, and the tag (lastest)
5. Add the environment variables for PostgreSQL via connection strings and restart the app service

## Demo
See the demo link: https://flaskdockerdemo-fdetcmbqd4aecjcw.eastus2-01.azurewebsites.net/

API endpoints:
- / - root message
- /health - check API health
- GET /items - retreive all items
- GET /items/:id - get specific item with id
- POST /items - add item record, include `name` in request body
- PUT /items/:id - update the item name with specific id, include `name` in request body
- DELETE /items/:id - delete the item with specific id

Request body format is JSON. For example, `{ "name": "GATECH EDM" }`
