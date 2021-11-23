#!/usr/bin/env python3

from aws_cdk import core


from test_pipeline.test_pipeline import MyPipelineStack


app = core.App()
MyPipelineStack(app, "test-pipeline-cdk")

app.synth()
