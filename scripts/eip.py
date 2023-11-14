ids=["i-017947c343c071d51", "i-03da349986804f2e3"]

import boto3
ec2 = boto3.client("ec2", region_name="us-west-2")

for id in ids:
    ins = ec2.describe_instances(InstanceIds=[id])
    info = ins["Reservations"][0]["Instances"][0]

    if "PublicIpAddress" in info:
        print(id, "Already assigned", info["PublicIpAddress"])
        continue

    priv_ip = info["PrivateIpAddress"]
    network_ifs = info["NetworkInterfaces"]
    network_if_id = ""
    for i in network_ifs:
        if priv_ip == i["PrivateIpAddress"]:
            network_if_id = i["NetworkInterfaceId"]
            break

    if network_if_id:
        allocation = ec2.allocate_address(Domain='vpc', TagSpecifications=[{'ResourceType': 'elastic-ip',"Tags":[{"Key":"Name", "Value":"pzesheng_p5_efa"}]}])
        response = ec2.associate_address(
            AllocationId=allocation['AllocationId'],
            NetworkInterfaceId=network_if_id)

        print(id, allocation["PublicIp"])
