#!/usr/bin/python
import ConfigParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.elastictranscoder 
import json
from pprint import pprint


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
    print "Connecting to S3..."
    return connection

'''
Opens a bucket
@param Connection to aws 
@param name of the bucket to open
@return the specified bucket
'''
def openBucket(connection, bucketName):
    bucket = connection.get_bucket(bucketName)
    print "Opening" +" " +bucketName +" " +"bucket"
    return bucket

'''
Uploads Files to a Amazon S3 Bucket
@param Name of bucket to upload files
@param Credentials for the AWS Account
@return The name of the video
'''
def uploadToBucket(bucket,key,fileName):
    
    print "Uploading to bucket"
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
    print "Connecting to AWS Elastic Transcoder"
    
    transcode =  boto.elastictranscoder.connect_to_region('us-west-2') #connect to elastic transcoder
    
    print "Configuring Job"

    pipelineId = '1369250428778-u8cpzw' #Id of aws pipeline
    
    presetList = transcode.list_presets() #dict of all available presets
    
    presets = {} #dictionary for each preset {presetId:description}
    outputs = [] #output list of dictionarys for a transcoder job
    

    numberOfPresets = 3 #first n presets in the list

    #Grab the Id and Description of each n presets in a range
    for x in range(numberOfPresets):
        presetId =  str(presetList['Presets'][x]['Id'])

        try:
            description = str(presetList['Presets'][x]['Description'])

        except TypeError, e:
            description = "unknown"
            
        
#make description string lowercase with no spaces
            description = ''.join(c.lower() for c in description if not c.isspace())
        #add the description to the dictionary
        presets.update({presetId:description}) 

    
    print "Creating job"
    
    transInput = {
        'Key': path,
        'FrameRate': 'auto',
        'Resolution': 'auto',
        'AspectRatio': 'auto',
        'Interlaced': 'auto',
        'Container': 'auto'
        }
    pprint (transInput)

    #Create a job for each desired preset
    for pId, descrip in presets.iteritems():
        
        transOutput = {
            
            'PresetId': pId,
            'Rotate': '0',
            'ThumbnailPattern': "",            
            'Key': path +"-" + descrip
            }

        outputs.append(transOutput)
        

        
    pprint (outputs)

    try:
        transcode.create_job(pipelineId, transInput, outputs=outputs)
    except Exception, e:
        print e
        

    
def main():
    #Load credentials
    configFileLocation = "/home/cygnss/.boto"
    credentials = getCredentials(configFileLocation)
    
    #Connect to aws
    conn = setConnection(credentials)



    #Upload a file to the bucket
    key = "transcodeTest1"
    '''
    fileName = "video.mp4"
    bucketName = "tfotl"
    bucket = openBucket(conn, bucketName)
    uploadToBucket(bucket,key,fileName)
    '''

    #Transcode a file
    transcodeVideo(key)
    



if __name__ == "__main__":
    main()
