import os

from aws_cdk import (
	core,
	aws_ecr,

)


class CdkFlaskEcrStack(core.Stack):

	def __init__(
		self, 
		scope: core.Construct, 
		construct_id: str,
		**kwargs
	) -> None:

		super().__init__(scope, construct_id, **kwargs)


		self.ecr_repo = aws_ecr.Repository(
			self, 'cdk-flask-app.repo2',
			repository_name='cdk-flask.app-repo',
			removal_policy=core.RemovalPolicy.DESTROY,	
		)
		
