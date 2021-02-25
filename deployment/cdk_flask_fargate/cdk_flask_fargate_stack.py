import os

from aws_cdk import (
	core,
	aws_ecr,
	aws_ec2,
	aws_ecs,
	aws_ecs_patterns,
	aws_dynamodb,
)


class CdkFlaskFargateStack(core.Stack):

	def __init__(
		self, 
		scope: core.Construct, 
		construct_id: str,
		ecr_repo: aws_ecr.Repository,
		**kwargs
	) -> None:
		
		super().__init__(scope, construct_id, **kwargs)

        	# The code that defines your stack goes here

		dynamodb_table = self.create_ddb_table()

		vpc = aws_ec2.Vpc(self, 'TheVPC',
			cidr='10.0.0.0/16'
		)
		
		vpc.apply_removal_policy(
			policy=core.RemovalPolicy.DESTROY
		)


		image = aws_ecs.ContainerImage.from_ecr_repository(
			repository=ecr_repo,
		)

		cluster = aws_ecs.Cluster(self, 'cdk-flask.cluster',
			vpc=vpc,
		)

		cluster.apply_removal_policy(
			policy=core.RemovalPolicy.DESTROY
		)

		task = aws_ecs.FargateTaskDefinition(
			self,
			'cdk-flask.fargate-task',
			memory_limit_mib=512,
			cpu=256,
			#environment=[['DYNAMODB_TABLE_NAME', dynamodb_table.table_arn]]
		)

		container = task.add_container('cdk-flask_container',
			image=image,
			environment=['DYNAMODB_TABLE_NAME', dynamodb_table.table_arn]

		)

		container.add_port_mappings(
			aws_ecs.PortMapping(
				host_port=5143,
				container_port=5143
			)
		)

		fargate = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
			self, 'cdk-flask.fargate',

			cluster=cluster,
			task_definition=task,
			task_subnets=aws_ec2.SubnetSelection(
				subnets=vpc.private_subnets
			)
		)


	def create_ddb_table(self):
		dynamodb_table = aws_dynamodb.Table(
			self, 'Users',
			partition_key=aws_dynamodb.Attribute(
				name='username',
				type=aws_dynamodb.AttributeType.STRING
			),
			removal_policy=core.RemovalPolicy.DESTROY,
			table_name='ssm-cdk_flask_users-dev'
		
		)

		core.CfnOutput(
			self,
			'AppTableName',
			value=dynamodb_table.table_name
		)

		return dynamodb_table

