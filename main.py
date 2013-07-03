#!/usr/bin/python
import ConfigParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.elastictranscoder import layer1


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
Connects to AWS
@param Secret Key ID and password tuple
@return connection to S3
'''
def setConnection(credentials):
    #Connect
    connection = S3Connection(credentials[0],credentials[1])
    return connection

'''
Opens a bucket
@param Connection to aws 
@param name of the bucket to open
@return the specified bucket
'''
def openBucket(connection, bucketName):
    bucket = connection.get_bucket(bucketName)
    return bucket

'''
Uploads Files to a Amazon S3 Bucket
@param Name of bucket to upload files
@param Credentials for the AWS Account
@return The name of the video
'''
def uploadToBucket(bucket,key,fileName):
    
    #Upload File
    k = Key(bucket)
    k.key = key
    k.set_contents_from_filename(fileName)
    return k.key

'''
Transcodes a video
@param The name of the video in the bucket
'''
def transcodeVideo(key):

    pipeline = "Standard Sermon"
    outputName = key + "Trans"
    

    transcode = layer1.ElasticTranscoderConnection()
    transcode.create_job(pipeline, key, outputs = outputName  )
    
def main():
    #Load credentials
    configFileLocation = "/home/xv11/.boto"
    credentials = getCredentials(configFileLocation)
    
    #Connect to aws
    conn = setConnection(credentials)


    #Upload a file to the bucket
    key = "testVideo2"
    fileName = "video.mp4"
    bucketName = "tfotl"
    bucket = connectToBucket(conn, bucketName)
    uploadToBucket(bucket,key,fileName)

    #Transcode a file
    
    



if __name__ == "__main__":
    main()
