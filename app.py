#!/usr/bin/env python3
import aws_cdk as cdk
from CF.CF_stack import CFStack
from code.codepipestack import Pipeline
from code.codestack import CodecommitStack
from Route53.Route53 import Route53Stack
from storage.bucket_lambda import S3LambdaStack
from acm.acm_skack import AcmStack



app = cdk.App()
code = CodecommitStack(app, 'codecommit', code_dir="sources")
s3la_stack = S3LambdaStack(app, "s3-la-stack")
cf_stack = CFStack(app, "cf", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
pipeline = Pipeline(app, 'pipeline', s3bucket=cdk.Fn.import_value("Calculator-bucket"))
route53 = Route53Stack(app, "Route-53", env=cdk.Environment(account="174851338573", region="eu-central-1"))
#acmstack = AcmStack(app, "acmstack"   )

cf_stack.add_dependency(s3la_stack)
pipeline.node.add_dependency(cf_stack)
route53.add_dependency(pipeline)


app.synth()