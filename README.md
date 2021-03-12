# Machine learning engineering project

## Overview of the solution

![alt text](https://cdn-images-1.medium.com/max/1000/1*NmuZ3pjxuX3sdw09ONVFCA.png)

## Requirements

* An AWS account
* AWS CLI
* A Github account
* Python 3.7 or greater
* a scikit-learn model trained and serialized with its preprocessing step (using pickle)


## How is the infrastructure deployed?
It is possible to configure the infrastructure via the AWS console but here we will use a Github action that I wrote which will allow us to deploy a model without having to manage the deployment of the infrastructure except for the s3 bucket.
The GitHub action uses the serverless framework under the hood in order to package the fast REST API, the prediction worker, and takes care of deploying the underlying infrastructure.

## Setting up the project
I will use poetry to set up the project structure and manage dependencies, feel free to adapt it if you want to use pip with a virtual environment.
1. Create a new project with poetry new <name_of_project>
2. cd to the created folder
3. Run the following command to install the project's dependencies : `poetry add pandas scikit-learn pydantic typer boto3`
4. Create an app.py file in <your_package_name> folder that is in your root directory.

## Setting aws 

1. `poetry run cli create-bucket <bucket-name-to-be-created>`
2. `poetry run cli upload <bucket-name> <path_to_your_model> --tag 1.0`
3. `poetry run cli list-objects <bucket-name> `

## Creating the validation schema

As the GitHub action uses FastApi under the hood, we need to provide a class for the post method that will handle the data the client will submit to prediction. Thanks to the definition of that class, FastApi will handle the validation of the submitted data for us.
Create a validation.py in the root folder, your class must respect the order, names as well as the data type of the raw data you used to train your model. see here a class example.

## Testing the model
The test suite first ensures that the validation class we wrote can be initialized with the raw data. Then it tests that the model is an instance of the scikit learn Pipeline class. Finally, it makes sure that our model can predict the raw data.
 `poetry run pytest -v`

## Configure web app form
see here a config file example

## Configure the github workflow

The following secrets are needed:
1. AWS_ACCESS_KEY
2. AWS_KEY_ID
3. ACCESS_TOKEN

The first two are your AWS ids that are needed to connect to AWS from the CLI. For the last one, you will need to create a GitHub personal access token, click here to see how to generate one.
You will need to select the scopes you'd like to grant this token, make sure to select the repo checkbox to be able to deploy the form to GitHub page.
Now you need to create secrets inside your GitHub repository so that actions can use them, check the official documentation here to see how to proceed

## Deploy

Just push the repo to github and check the action tab. When done go to https://<your_github_name>.github.io/<your_repo_name>/#/. you should see a home page.

## Interacting through the FAST API Endpoint
You can find the API endpoint address in the log of the GitHub action by clicking in the step "API rest deployment" or in the AWS console in the API gateway service.
The endpoint provides two services:
* POST - <your_adress>/<stage>/api/predict that accept the data as defined in the raw_data in our test suite and it returns a prediction_id
* GET - <your_adress>/<stage>/api/predict/<prediction_id> that return the prediction result
  
