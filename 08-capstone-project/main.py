import boto3

aws_access_key_id = "ASIARC3CKZR2UOPOSJMU"
aws_secret_access_key = "jYq7lXRw4OMvJ+f1TXsdnQMT+eBN4TfTRx3irP/5"
aws_session_token = "FwoGZXIvYXdzEAcaDDgO+f4wWHiph48Q9iLPAfkBEt2v1LmgfifRNhJ97UwhpZUwtya6Rwg35mk1zHd6iGEJwYdPXBYLBBei7bBGs08rYNcvJUDEuLM2AHdOlacInDjvS1/iB/u+sW1RIx4FiysvGUPJ2WjmY5Vd09zoDnFau6/FG8trUIueChui0ZGXKKDygvBT1CA4rKp3jcn1Hu3ZgWKy6xEQBG7+ldfThepIdMMUewB9eZFq/mQcMRBu0a2pTAbyq9rVrHz4CWJaekKCuH/ECdUuzm7501bhbE/ujMWojc0GeM+D2Zp47Si3l/ecBjIthMOHoZ/y3cVg1jKG07pNEIqeb4wub0vMjgx+07+snSnX+Uj0n1ViqrUK1p5Q"

s3 = boto3.resource(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
s3.meta.client.upload_file(
    "HRDataset_v14.csv",
    "kik-bucket-public",
    "HRDataset_v14.csv",
)



# client = boto3.client(
#     "s3",
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_session_token=aws_session_token
# )
#print(client)
# response = client.list_objects(
#     Bucket = "kikbucket",
#     MaxKeys=2,
# )
#print(response["Contents"])
# contents = response["Contents"]
# for content in contents:
#     print(content["Key"], content["Size"])

