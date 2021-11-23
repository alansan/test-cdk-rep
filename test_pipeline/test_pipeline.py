from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from aws_cdk.aws_lambda import Function, InlineCode, Runtime
import os

class MyPipelineAppStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = MyLambdaStack(self, "LambdaStack")

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Function(self, "LambdaFunction", 
            runtime=Runtime.NODEJS_12_X,
            handler="index.handler",
            code=InlineCode("exports.handler = _ => 'Hello, CDK';")
        )
        
class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.git_hub("alansan/test-cdk-rep", "master"),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        ),
                        cross_account_keys=False
                    )

        test_stage = pipeline.add_stage(MyPipelineAppStage(self, "test"))