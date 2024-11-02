import boto3
import json
import cfnresponse

def lambda_handler(event, context):
    acm = boto3.client('acm')
    
    # Log the incoming event for debugging
    print("Received event:", json.dumps(event))

    try:
        domain_name = event['ResourceProperties']['DomainName']
        response = acm.list_certificates(CertificateStatuses=['ISSUED'])
        certificates = response['CertificateSummaryList']

        for cert in certificates:
            if domain_name in cert['DomainName']:
                cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                    'CertificateArn': cert['CertificateArn']
                })
                return

        raise Exception(f"{domain_name} için uygun sertifika bulunamadı")

    except Exception as e:
        print("Error:", str(e))
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            'Reason': str(e)
        })


# Yerel test için örnek bir event ve context oluşturma
if __name__ == "__main__":
    test_event = {
        "ResourceProperties": {
            "DomainName": "gokanmalkoc.click"
        },
        "ResponseURL": "http://example.com",  # Fake URL for testing
        "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/my-stack/abcdef01-2345-6789-abcd-ef0123456789",  # Fake Stack ID for testing
        "RequestType": "Create",
        "LogicalResourceId": "MyResource",
        "RequestId": "unique-request-id"  # Fake Request ID for testing
    }
    
    # Lambda context nesnesini simüle etme
    class Context:
        def __init__(self):
            self.function_name = "TestFunction"
            self.memory_limit_in_mb = 128
            self.aws_request_id = "test_request_id"
            self.invoked_function_arn = "arn:aws:lambda:region:account-id:function:TestFunction"
            self.log_group_name = "/aws/lambda/TestFunction"
            self.log_stream_name = "2024/11/01/[$LATEST]abcdef1234567890"

    context = Context()
    
    # Fonksiyonu test etme
    lambda_handler(test_event, context)
