from aws_cdk import (
    core,
    aws_lambda as _lambda
)
from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as codepipeline_actions,
    
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep


class LambdaStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('test_pipeline/lambda'),
            handler='hello.handler',
        )


class DeployStage(core.Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        lambda_stack = LambdaStack(self, "LambdaStack")
        
        
class MyPipelineStack(core.Stack):
    def __init__(self, scope, id, *, description=None, env=None):
        super().__init__(scope, id, description=description, env=env)

        pipeline =  CodePipeline(self, "Pipeline", 
                        synth=ShellStep("Synth", 
                                        input=CodePipelineSource.git_hub("alansan/test-cdk-rep", "master"),
                                        commands=["npm install -g aws-cdk", 
                                        "python3 -m pip install -r requirements.txt",
                                        "cdk synth"]
                                        ),
                        cross_account_keys=False
                    )
    
        pipeline.add_stage(DeployStage(self, "deploy", env=env))