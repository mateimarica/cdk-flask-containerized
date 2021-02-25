# running



* In the `deployment` folder of this repo, run  `. venv/bin/activate`

* Do `cdk deploy cdk-flask-ecr-stack2`

* Go to https://console.aws.amazon.com/ecr/repositories and search for `cdk-flask.app-repo` and click on the repository. Click on `View push commands` in the top-right corner

* In the `docker` folder of this repo, run the four commands given in the `View push commands`, in order

* Go back to the `deployment` folder, do `cdk deploy cdk-flask-fargate-stack` (with the venv activated)
