# Cloud Providers: Amazon Bedrock & Google Cloud

OpenAI models can be provisioned through major enterprise cloud providers to satisfy strict data sovereignty, compliance (HIPAA, FedRAMP), and private networking requirements.

---

## 1. Amazon Bedrock Integration

Deploy OpenAI models directly within AWS VPCs:
- **IAM Authentication**: Eliminate static API keys; authenticate using AWS IAM roles and SigV4 request signing.
- **PrivateLink**: Route all inference traffic privately over AWS VPC endpoints without traversing the public internet.
- **CloudWatch Monitoring**: Stream token metrics, latency percentiles, and invoke errors to AWS CloudWatch.

---

## 2. Google Cloud Integration

Deploy OpenAI models natively inside Google Cloud projects:
- **Workload Identity**: Authenticate service accounts using Google Cloud IAM.
- **Cloud Audit Logs**: Maintain tamper-proof audit trails for compliance reporting.
- **Multi-Cloud Disaster Recovery**: Distribute inference load between direct OpenAI endpoints, AWS, and GCP.
