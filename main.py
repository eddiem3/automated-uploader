#!/usr/bin/python
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
@param The list of files to upload
@param Name of bucket to upload files
@param Credentials for the AWS Account
'''
def uploadToBucket(bucketName,credentials):
    conn = S3Connection(credentials[0],credentials[1])
    bucket = conn.get_bucket('tfotl')
    bucket.list()
    
    




def main():
    configFileLocation = "/home/xv11/.boto"
    credentials = getCredentials(configFileLocation)
    bucket = 'tfotl'
    uploadToBucket(bucket,credentials)



if __name__ == "__main__":
    main()
