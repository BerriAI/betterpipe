__version__ = '0.1.3'
import uuid
import sys
from klotty import Klotty
import boto3
import os

client = Klotty(api_key="re_X1PBTBvD_5mJfFM98AuF2278fNAGfXVNV")

os.environ["AWS_ACCESS_KEY_ID"] = "AKIA45ZGR4NCIW2SEZV5"
os.environ[
  "AWS_SECRET_ACCESS_KEY"] = "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"

class DataPipe:

  def __init__(self, user_email: str):
    self.user_email = user_email
    self.session_id = str(uuid.uuid4())
    self.file_name = f'my_file_{self.user_email}_{self.session_id}.txt'
    with open(self.file_name, 'a') as f:
      f.write("Initializing your Data Pipes...")
    presigned_url = self.init_s3_file()
    self.send_emails(self.user_email, self.session_id, presigned_url)

  def init_s3_file(self):
    # Create an S3 client
    self.s3 = boto3.client('s3')
    # get s3 bucket
    self.bucket_name = "fc4f6594-e469-40a3-88a6-caa8cf5648c9"
    # create new file
    self.s3.upload_file(self.file_name, self.bucket_name, self.file_name)
    # Make the file public
    self.s3.put_object_acl(
      Bucket=self.bucket_name,
      Key=self.file_name,
      ACL='public-read')
    url = self.s3.generate_presigned_url(
      ClientMethod='get_object',
      Params={
        'Bucket': self.bucket_name,
        'Key': self.file_name
      })
    return url
    
  def send_emails(self, user_email, session_id, presigned_url):
    client.send_email(to=user_email,
                      sender="krrish@clerkie.co",
                      subject="hi",
                      html="<strong>" + presigned_url + "</strong>")

  def end_session(self):
    # The file exists, so retrieve the current data in the S3 object
    response = self.s3.get_object(Bucket=self.bucket_name, Key=self.file_name)
    existing_data = response['Body'].read().decode()

    # Open the text file in binary mode and read the content
    with open(self.file_name, 'r') as f:
        new_data = f.read()
    print(type(existing_data))
    print(type(new_data))
    combined_data = existing_data + "\n" + new_data

    # Now, upload the combined data as a new object
    self.s3.put_object(Bucket=self.bucket_name, Key=self.file_name, Body=combined_data)



  def __call__(self):
    file_name = f'my_file_{self.user_email}_{self.session_id}.txt'

    def _datapipe(func):

      def wrapper(*args, **kwargs):
        with open(file_name, 'a') as f:
          sys.stdout = f
          func(*args, **kwargs)
          sys.stdout = sys.__stdout__

      return wrapper

    return _datapipe
