# 1. Install the Databricks SDK (if you haven't already)
#    %pip install databricks-sdk

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json

# 2. Prepare your data (you can also load these from files if you prefer)
mitre_json = {
  "ID": "T1098.003",
  "STIX ID": "attack-pattern--2dbbdcd5-92cf-44c0-aea2-fe24783a6bc3",
  "name": "Account Manipulation: Additional Cloud Roles",
  "description": "An adversary may add additional roles or permissions …",
  "url": "https://attack.mitre.org/techniques/T1098/003",
  "created": "19 January 2020",
  "last modified": "15 April 2025",
  "domain": "enterprise-attack",
  "version": 2.5,
  "tactics": "Persistence, Privilege Escalation",
  "detection": "Collect activity logs from IAM services and cloud administrator accounts …"
}

spl_query = r"""
index=cloud_infra_aws sourcetype=aws:cloudtrail eventName=AddUserToGroup requestParameters.groupName=*admin*
| rename userIdentity.arn as arn, userIdentity.userName as src_userName
| eval arn=mvindex(split(arn,"/"),-1)
| eval src_userName=coalesce(src_userName,arn)
| table _cd_time,action,aws_account_id,aws_account_name,awsRegion,status,eventName,sourceIPAddress,userAgent,eventType,
  src_userName,requestParameters.userName,requestParameters.groupName
| rename requestParameters.userName as user, sourceIPAddress as src, requestParameters.groupName as group
| eval dest_user=user
| eval signature="User was added to group."
| eval search_title="Access - CRO - AWS New Admin Addition"
| `RBA_add_uid`
| `RBA_CE_normalize`
| `uc_cro_activity_tagging`
"""

read_me = """
# 1001 AWS New Admin Addition

*Monitor potentially unwanted additions of users to admin-related groups in AWS.*

## Objective
Highlight when a user is added to a group whose name contains “admin.”

## Data Sources
AWS CloudTrail logs (AddUserToGroup events).

https://docs.aws.amazon.com/awscloudtrail/latest/userguide/how-cloudtrail-works.html

### Filters
- eventName=AddUserToGroup
- requestParameters.groupName=.*admin.*
"""

# 3. Build the chat prompt
system_msg = ChatMessage(role=ChatMessageRole.SYSTEM, content=(
    "You are a security-focused assistant. "
    "Your first task is to review the provided SPL query against the MITRE ATT&CK technique JSON "
    "and suggest any changes needed to fully detect that technique. "
    "Your second task is to generate a refined, production-ready README based on the draft."
))

user_content = (
    "### MITRE ATT&CK Technique\n"
    f"```json\n{json.dumps(mitre_json, indent=2)}\n```\n\n"
    "### SPL Query\n"
    f"```spl\n{spl_query}\n```\n\n"
    "### README Draft\n"
    f"{read_me}\n\n"
    "Please:\n"
    "1. Tell me if the SPL needs any adjustments to match the described technique (and show the updated SPL if so).\n"
    "2. Generate a polished README that includes all necessary sections (description, technique mapping, query explanation, fields, signature, etc.)."
)

user_msg = ChatMessage(role=ChatMessageRole.USER, content=user_content)

# 4. Call the LLM
w = WorkspaceClient()
response = w.serving_endpoints.query(
    name="databricks-meta-llama-3-3-70b-instruct",
    messages=[system_msg, user_msg],
    temperature=0.1,
    max_tokens=2048
)  # 

# 5. Print out what the LLM returns
print(response.choices[0].message.content)
