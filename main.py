#!/usr/bin/python
import ConfigParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.elastictranscoder 
import json
from pprint import pprint

class AWSTools(self):

    '''
    Loads the username and password for amazon aws from a config file
    And makes an aws connection
    @param Location of the config file
    
    '''
    def __init__(self):
        configFileLocation = "/home/neumann/.boto"
        config = ConfigParser.ConfigParser()
        config.read (configFileLocation)

        print "Loading user credenials..."

        userName = config.get('Credentials','aws_access_key_id')
        password = config.get('Credentials','aws_secret_access_key')

        print "Connecting to S3 Bucket..."
        self.connection = S3Connection(credentials[0],credentials[1])

    '''
    Opens a bucket
    @param Connection to aws 
    @param name of the bucket to open
    @return the specified bucket
    '''
    def openBucket(self, bucketName):
        bucket = self.connection.get_bucket(bucketName)
        print "Opening" +" " +bucketName +" " +"bucket"
        return bucket

    '''
    Uploads Files to a Amazon S3 Bucket
    @param Name of target bucket
    @param File Key
    @return File Name
    '''
    def uploadToBucket(bucket,key,fileName):
        
        print "Uploading to bucket"
    
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



class Publisher:
    
    def __init__(self, paths, keys, bucket):

        self.paths = paths
        self.keys = keys
        self.bucket = bucket


    def makeShortUrl(self):
        return None

    def postFacebook(self):
        return None

    def postTwitter(self):
        return None

    def postYoutube(self):

    def postS3(self):
        AW
        return None

    def transcodeVideo(self):
        return None



        
def main():
    
    #Load user data
    parser = argparse.ArgumentParser(description='Media Uploader')
    parser.add_argument('-i','--input', help = 'List of file paths', nargs='*', required = True)
    parser.add_argument('k', '--key', help = 'Keys for corresponding file paths, if unspecified then key = input', nargs='*',required = False)
    parser.add_argument('b', '--bucket', help = 'S3 Bucket to upload to', required = True)
    args = parser.parse_args()

    inputPaths = args.input
    inputKeys = args.key
    bucket = args.bucket
    

    if len(inputKeys) != 0:
        if len(inputKeys) != len(inputPaths):
            print "Error: Each file does not have a corresponding key"
            
    if len(inputKeys) == 0:
        inputKeys = inputPaths


    #Load aws credentials
    configFileLocation = "/home/cygnss/.boto"

    #Connect to aws
    conn = connectToS3(configFileLocation)
    


    



if __name__ == "__main__":
    main()
