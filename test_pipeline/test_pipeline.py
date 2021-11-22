from aws_cdk import (
    core,
    aws_lambda as _lambda
)
from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines
)


# The stacks for our app are minimally defined here.  The internals of these
# stacks aren't important, except that DatabaseStack exposes an attribute
# "table" for a database table it defines, and ComputeStack accepts a reference
# to this table in its properties.
#

class LambdaStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

#
# Stack to hold the pipeline
#
class MyPipelineStack(core.Stack):
    def __init__(self, scope, id, *, description=None, env=None):
        super().__init__(scope, id, description=description, env=env)

        # synth=pipelines.CodeBuildStep('synth_rizwan', input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        # , "cdk synth"] ,primary_output_directory='infra/cdk.out', role= cbRole)
        
        pipeline = pipelines.CodePipeline(self, "Pipeline")

        # 'MyApplication' is defined below. Call `addStage` as many times as
        # necessary with any account and region (may be different from the
        # pipeline's).
        pipeline.add_stage(MyApplication(self, "Prod",
            env=env
            )
        )

#
# Your application
#
# May consist of one or more Stacks (here, two)
#
# By declaring our DatabaseStack and our ComputeStack inside a Stage,
# we make sure they are deployed together, or not at all.
#
class MyApplication(core.Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        lambda_stack = LambdaStack(self, "Database")

