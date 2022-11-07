import ibm_boto3
from ibm_botocore.client import Config, ClientError


class cloudstorage():
    COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
    COS_API_KEY_ID = "ogOO6QboQdmgmMhvhBWOAxZ6KZPSNku2-6f1i0YlDyqg"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/acefc5aff7374e68b4d4d9c345ade419::serviceid:ServiceId-084f8b9f-2f0c-4863-9387-b5985cbb15ec"
    cos = ibm_boto3.resource("s3",
                             ibm_api_key_id=COS_API_KEY_ID,
                             ibm_service_instance_id=COS_INSTANCE_CRN,
                             config=Config(signature_version="oauth"),
                             endpoint_url=COS_ENDPOINT)
    print(cos)

    def get_bucket_contents(self,bucket_name):
        print("Retrieving bucket contents from: {0}".format(bucket_name))
        try:
            files = self.cos.Bucket(bucket_name).objects.all()
            files_names = []
            for file in files:
                files_names.append(file.key)
                print("Item: {0} ({1} bytes).".format(file.key, file.size))
            return files_names
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to retrieve bucket contents: {0}".format(e))
            
    def delete_item(self,bucket_name, object_name):
        try:
            self.cos.Object(bucket_name,object_name).delete()
            print("Item: {0} deleted!\n".format(object_name))
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to delete object: {0}".format(e))
            
    def multi_part_upload(self,bucket_name, item_name, file_path):
        try:
            print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
            part_size = 1024 * 1024 * 5
            file_threshold = 1024 * 1024 * 15
            transfer_config = ibm_boto3.s3.transfer.TransferConfig(
                multipart_threshold=file_threshold,
                multipart_chunksize=part_size
            )
            with open(file_path, "rb") as file_data:
                self.cos.Object(bucket_name, item_name).upload_fileobj(
                    Fileobj=file_data,
                    Config=transfer_config
                )

            print("Transfer for {0} Complete!\n".format(item_name))
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to complete multi-part upload: {0}".format(e))
