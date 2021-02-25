#!/usr/bin/env python3

import os

from aws_cdk import core

from cdk_flask_ecr import CdkFlaskEcrStack
from cdk_flask_fargate import CdkFlaskFargateStack


env = core.Environment(
	account=os.environ['CDK_DEFAULT_ACCOUNT'],
	region=os.environ ['CDK_DEFAULT_REGION']
)
app = core.App()
core.Tags.of(app).add(
	key='project1',
	value='CCI'
)

ecr_stack_name = 'cdk-flask-ecr-stack2'
fargate_stack_name = 'cdk-flask-fargate-stack'

ecr_stack = CdkFlaskEcrStack(
	app, 
	ecr_stack_name,
	env=env
)

fargate_stack = CdkFlaskFargateStack(
	app,
	fargate_stack_name,
	ecr_repo=ecr_stack.ecr_repo,
	env=env
)

app.synth()
