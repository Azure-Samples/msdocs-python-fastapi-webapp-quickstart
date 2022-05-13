---
page_type: sample
description: "A minimal sample app that can be used to demonstrate deploying FastAPI apps to Azure App Service."
languages:
- python
products:
- azure
- azure-app-service
---

# Deploy a Python (FastAPI) web app to Azure App Service - Sample Application

This is the sample FastAPI application for the Azure Quickstart [Deploy a Python (Django, Flask or FastAPI) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python).  For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:
- Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
- Flask [https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart)

If you need an Azure account, you can [create on for free](https://azure.microsoft.com/en-us/free/).


To try the application on your local machine:

### Install the requrements
`pip install -r requirements.txt`

### Start the application
`uvicorn main:app --reload`

### Example call
http://127.0.0.1:8000/items/4?q=my%20test%20query

### Example json response
`{"item_id": 4, "q": "my test query"}`

To learn more about FastAPI, see [FastAPI](https://fastapi.tiangolo.com/).
