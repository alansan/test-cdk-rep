from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from cdk_pipeline.pipeline_app_stage import MyPipelineAppStage
import os

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.git_hub("timofeic/cdk-pipeline", "master"),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        ),
                        cross_account_keys=False
                    )

        pipeline.add_stage(MyPipelineAppStage(self, "test",
            env=cdk.Environment(account="644040437375",region="eu-central-1")))
