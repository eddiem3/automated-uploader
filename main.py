5B#!/usr/bin/python
import ConfigParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key


'''
Loads the username and password for amazon aws from a config file
@param Location of the config file
@return a tuple in the form (username, password)
'''
def getCredentials(configFileLocation):
    config = ConfigParser.ConfigParser()
    config.read (configFileLocation)
    
    userName = config.get('Credentials','aws_access_key_id')
    password = config.get('Credentials','aws_secret_access_key')
    
    return (userName, password)

    
'''
Uploads Files to a Amazon S3 Bucket
@param Name of bucket to upload files
@param Credentials for the AWS Account
'''
def uploadToBucket(bucketName,credentials):
    #Connect to bucket
    conn = S3Connection(credentials[0],credentials[1])
    bucket = conn.get_bucket(bucketName)
    
    #Upload File
    k = Key(bucket)
    k.key = 'testVideo'
    k.set_contents_from_filename('video.mp4')

def transcodeVideo():
    
    
    
    
    
    




def main():
    configFileLocation = "/home/xv11/.boto"
    credentials = getCredentials(configFileLocation)
    bucketName = 'tfotl'
    uploadToBucket(bucketName,credentials)



if __name__ == "__main__":
    main()
