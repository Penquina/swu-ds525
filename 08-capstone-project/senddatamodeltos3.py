#Upload datamodel files into s3

import boto3

aws_access_key_id = "ASIARC3CKZR2364Q5A63"
aws_secret_access_key = "Tnee/cn5c+u7ScgHVfulSkxjqo6KW4D5vViN0TT2"
aws_session_token = "FwoGZXIvYXdzEBgaDJy8QB9miJdz1p4jFCLPAQvjtehoiEIK27PaCPTde/tSBSeGBgia0FARRPRoC8rlwQvDiAPJZYlAgBDuIWifOV9W24aE0sDG9HAIC7UZk9JyIl/fjGMfzqVkSjXEHLNM/QcrhCL5aTiGljWZ/qiklXJCTBJNkci1aFlmTCP57y3BfbfE+uclGG3okcJ1CHAq8jtR/YoWZtHE7x5KRXrNpRmmNymq5pf1RQ/BS6He8M7Ov95sSZ12acYg6bCpPBMlrf20P/zkytsKirW1c8GwaGXBczPLZZ9wFGOBcEBhKCic4vqcBjIt0T3ht1+CEq6OQvUgG0RWngm0ZAF3Jk8QeZGaN7CMF5TLghJjNoPC0n0MHb+K"

s3 = boto3.resource(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
s3.meta.client.upload_file(
    "data/employee_details.csv",
    "kik-bucket-public",
    "employee_details.csv",
)

s3.meta.client.upload_file(
    "data/recruitment.csv",
    "kik-bucket-public",
    "recruitment.csv",
)

s3.meta.client.upload_file(
    "data/salary.csv",
    "kik-bucket-public",
    "salary.csv",
)

s3.meta.client.upload_file(
    "data/sex.csv",
    "kik-bucket-public",
    "sex.csv",
)
