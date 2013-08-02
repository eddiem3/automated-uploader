#!/usr/bin/python
import ConfigParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.elastictranscoder 
import urllib2
import json


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
def transcodeVideo(path):

    transcode =  boto.elastictranscoder.connect_to_region('us-west-2') #connect to elastic transcoder
    presetList = transcode.list_presets()
    
    presets = {}
    
    #Grab the Id and Description of each preset
    for x in range(3):
        presetId =  presetList['Presets'][x]['Id']

        description = presetList['Presets'][x]['Description']
        if description == None:
            description = "unknown"
        else:
#make description string lowercase with no spaces
            description = ''.join(c.lower() for c in description if not c.isspace())
        #add the description to the dictionary
        presets.update({presetId:description}) 

            pipelineId = '1369250428778-u8cpzw'
    
    transInput = {
        'Key': path,
        'FrameRate': 'auto',
        'Resolution': 'auto',
        'AspectRatio': 'auto',
        'Interlaced': 'auto',
        'Container': 'auto'
        }

    transOutput = {
        'Key': 'web' +path,
        'PresetId': '1351620000001-100070',
        'ThumbnailPattern': "",
        'Rotate': '0'
        }

    outputList = [transOutput,]

    #transcode.create_job(pipelineId, transInput, transOutput)


        
        

        
    






    #    presetList = json.loads(presetList)

    '''
    Todo: 
    Make a preset dictionary
    For each preset in the presetList
        grab the ID
        grab the Name -> remove spaces, convert to lowercase
        add to preset dictionary {Name:ID}

    For each item in the preset dictionary
        add make a new transOutput item -> with the key in the form of path +Name
        append the transOutput item to outputList
    createjob
    '''









    
def main():
    #Load credentials
    configFileLocation = "/home/cygnss/.boto"
    credentials = getCredentials(configFileLocation)
    
    #Connect to aws
    conn = setConnection(credentials)



    #Upload a file to the bucket
    key = "transcodeTest1"
    fileName = "video.mp4"
    bucketName = "tfotl"
    bucket = openBucket(conn, bucketName)
 #   uploadToBucket(bucket,key,fileName)

    
    

    #Transcode a file
    transcodeVideo(key)
    



if __name__ == "__main__":
    main()
