

# set the proper signature version in order not to get issues when generating URLs for encrypted files
aws configure set default.s3.signature_version s3v4

# do not forget to region parameter! (make sure it's the proper region you're choosing)
aws s3 presign s3://mybucket/myobject --region my-region

# add a custom expiration time
aws s3 presign s3://mybucket/myobject  --expires-in 300 --region my-region