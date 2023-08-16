import json
import boto3
from datetime import datetime
import tempfile
import uuid
from botocore.exceptions import ClientError
import time

s3 = boto3.resource('s3')
bucket = "bucketsimos"
key = "dataSismos.json"
obj = s3.Object(bucket, key)
body = obj.get()['Body'].read().decode('utf-8')
data = json.loads(body)

database = 'test-sks'
table = '"test-sks"'+ '.' + '"crawler_bucket_sks"'
output='s3://crawler-bucket-sks'
path='outputDataGET'


def lambda_handler(event, context):
    
    #print(event)
    
    if event["httpMethod"] == 'GET':
        
        client = boto3.client('athena')
        
        country = event['queryStringParameters'].get('country') 
        dateLower = event['queryStringParameters'].get('dateLower',0)
        dateUpper = event['queryStringParameters'].get('dateUpper',0)
        magnitudeLower = float(event['queryStringParameters'].get('magnitudeLower', 0))
        magnitudeHigher = float(event['queryStringParameters'].get('magnitudeHigher', float('inf')))
        skip = int(event['queryStringParameters'].get('skip', 0))
        
        #Transform date from yyyy/mm/dd to Unix format
        dateLower = int(datetime.strptime(dateLower, "%Y-%m-%d").timestamp())
        dateUpper = int(datetime.strptime(dateUpper, "%Y-%m-%d").timestamp())

        
        
        sql_query = f"""
        SELECT timestamp, country, magnitude
        FROM {table}
        WHERE country = '{country}'
        AND timestamp >= {dateLower} AND timestamp <= {dateUpper}
        AND magnitude >= {magnitudeLower} AND magnitude <= {magnitudeHigher}
        ORDER BY timestamp ASC
        OFFSET {skip}
        LIMIT 100
        """
        
        #print(sql_query)
        
        # Execution
        response = client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                # first {} contains the output variable, then adds a '/' character for the directory and then the path variable
                'OutputLocation': "{}/{}".format(output, path),
            }
        )
        
        execution_id: str = response["QueryExecutionId"]
        
        #Athena can only query 100 data points at a time, the following code lets it run the full partition before returning the results
        while True:
            try:
                result = client.get_query_results(QueryExecutionId=execution_id)
                break
            except ClientError as e:
                time.sleep(5)
        
        #print(result)
        
        keys = ["timestamp", "country", "magnitude"]
        parsed_result = []

        for entry in result["ResultSet"]["Rows"][1:]:
            parsed_entry = {}
            for i, value_dict in enumerate(entry["Data"]):
                parsed_entry[keys[i]] = value_dict["VarCharValue"]
            parsed_result.append(parsed_entry)
            
        #print(parsed_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps(parsed_result)
        }
    
    elif event["httpMethod"] == 'POST':
        body = json.loads(event['body'])
        
        sismos = body["sismos"]
        
        arrsismos = []
        
        for sismo in sismos:
            timestamp = sismo.get('timestamp')
            country = sismo.get('country')
            magnitude = sismo.get('magnitude')
            
            
            arrsismos.append({
                "timestamp": timestamp,
                "country": country,
                "magnitude": magnitude
            })
            # Convert the list of dictionaries to a JSON-formatted string
            json_string = "\n".join(json.dumps(item) for item in arrsismos)          
            
        #print(json_string)
        
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            json.dump(json_string, temp_file)
            
        filename = "dataJsonPOST/"+ uuid.uuid4().hex + ".json"
        
        s3.Bucket("crawler-bucket-sks").put_object(Key=filename,Body=json_string)
        
        return {
            'statusCode': 200,
            'body': json.dumps(json_string)
        }
        


    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'HTTP method not allowed'})
        }

