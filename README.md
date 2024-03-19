# Bedrock - Claude3 Samples

## About

These are some sample programs that I created to verify calling Claude3 from Python via boto3 on Bedrock.

> [!NOTE]
> I made this because I needed it, but I do not recommend it because there is not much advantage to using it via Amazon Bedrock. It is better to use the Claude API directly.

## Getting Started

### Prerequisite

- Python3
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Click](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiK0-mA1fWEAxWtm68BHdb_BRwQFnoECBIQAQ&url=https%3A%2F%2Fclick.palletsprojects.com%2F&usg=AOvVaw3frT-9FxWZIrQx3WVNwkzg&opi=89978449)
- [DotEnv](https://pypi.org/project/python-dotenv/)

### Installation

Since this is a sample code, installation automation is not implemented. Please set up the execution environment with the following steps.

1. Clone this repository to your local environment
2. Set up the Python `venv` environment
   ```sh
   $ cd [your local repository]
   $ python -m venv venv
   $ souce venv/bin/activate
   ```
3. Install prerequisite packages
   ```sh
   $ pip3 install boto3 click python-dotenv
   ```
4. From AWS management console, activate Anthropic - Claude3 from Amazon Bedrock - Model Access. Confirm that the Region is `us-west-2` at this time.
5. On the AWS management console, create a user from IAM (Identity and Access Management) and attach the `AmazonBedrockFullAccess` policy to that user.
6. Create an Access key for the user you created on IAM (Identity and Access Management). Save the generated access key and secret access key in the `~/.env` file as follows.
   ```toml
    AWS_ACCESS_KEY="[your access key]"
    AWS_SECRET_KEY="[your secret access key]"
   ```

## Usage

### awsfig

This sample code generates Typescript for CDK from an image of an AWS architecture diagram. In addition to text, it takes an image as input, making it a multimodal sample code.

````sh
$ ./awsfig.py -f aws.png
To realize the architecture depicted in the image using the AWS CDK in TypeScript, you can follow this code structure:

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

class MyInfrastructureStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a VPC
    const vpc = new ec2.Vpc(this, 'MyVPC', {
      maxAzs: 3, // Create resources in 3 Availability Zones
      natGateways: 1, // Enable NAT Gateways for outbound internet access
    });

    // Create public and private subnets
    const publicSubnets = vpc.publicSubnets;
    const privateSubnets = vpc.privateSubnets;

    // Create an Elastic Load Balancing (ELB)
    const elb = new elbv2.ApplicationLoadBalancer(this, 'MyELB', {
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC, // ELB should be in public subnets
      },
      internetFacing: true, // Internet-facing ELB
    });

    // Create an EC2 instance in each private subnet
    privateSubnets.forEach((subnet, index) => {
      new ec2.Instance(this, `MyEC2Instance${index}`, {
        vpc,
        vpcSubnets: { subnets: [subnet] },
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
        machineImage: ec2.MachineImage.latestAmazonLinux(),
      });
    });
  }
}

const app = new cdk.App();
new MyInfrastructureStack(app, 'MyInfrastructureStack');
```

This code will create the following resources:

1. A new VPC with 3 Availability Zones, public and private subnets, and NAT Gateways.
2. An Application Load Balancer in the public subnets, accessible from the internet.
3. An EC2 instance in each private subnet, which can communicate with the internet through the NAT Gateways.

Note that this code assumes you have the AWS CDK and its dependencies installed and configured correctly. Additionally, you might need to modify the code to match your specific requirements, such as instance types, security groups, and other configurations.

````

### translate

This will perform text translation. Even without specifying the source and target languages, it will determine the language of the input text, and properly select the source and target languages to perform the translation.

```sh
$ ./translate.py
Enter the text you wish to translate：Your inputs are not shared or leaked into any 3rd party and is safe for internal usage for up to highly confidential data.
入力されたデータは第三者に共有または漏洩されることなく、極秘情報を含む内部利用においても安全です。
```

### genolpqa

This will generate questions to check capabilities regarding one of the Principles of Amazon Organizational Leadership Program (OLP).

```sh
$ ./genolpqa.py
Select the OLP by number for which you wish to generate questions.
1 : Customer Obsession
2 : Ownership
3 : Invent and Simplify
4 : Are Right, A Lot
5 : Learn and Be Curious
6 : Hire and Develop the Best
7 : Insist on the Highest Standards
8 : Think Big
9 : Bias for Action
10 : Frugality
11 : Earn Trust
12 : Dive Deep
13 : Have Backbone; Disagree and Commit
14 : Deliver Results
15 : Strive to be Earth’s Best Employer
16 : Success and Scale Bring Broad Responsibility
>>Generating questions about Are Right, A Lot.
```

```markdown
### Main Questions

1. Can you share an experience where you relied on data and insights to challenge a widely accepted idea or approach within your organization?

   - What specific data or insights did you leverage?
   - How did you present your findings to stakeholders and convince them to consider an alternative approach?
   - What were the outcomes of implementing the new approach, and how did it improve upon the previous method?

2. Describe a situation where you had to make a difficult decision based on incomplete or ambiguous data.

   - How did you evaluate the available information and identify the gaps or areas of uncertainty?
   - What risk mitigation strategies did you employ to account for the unknowns?
   - How did you communicate the decision and rationale to those impacted, and how did you address any concerns or resistance?

3. Can you provide an example of when you proactively sought out diverse perspectives and used them to inform your decision-making process?

   - How did you identify and engage individuals with different backgrounds, experiences, or viewpoints?
   - What challenges did you encounter in synthesizing the diverse perspectives, and how did you overcome them?
   - How did incorporating diverse perspectives enhance the quality of your decision or solution?

4. Have you ever encountered a situation where your data-driven approach conflicted with company policies or industry norms?

   - How did you navigate the tension between data-driven insights and established practices or regulations?
   - What steps did you take to ensure compliance while still leveraging data to drive innovation or optimization?
   - How did you communicate the rationale for your approach to stakeholders, and what was the outcome?

5. Can you describe a time when you had to make a decision quickly based on limited data due to time constraints?

   - What was the nature of the time-sensitive situation, and what were the potential consequences of inaction?
   - How did you prioritize and analyze the available data to extract meaningful insights within the given timeframe?
   - What safeguards or contingency plans did you put in place to mitigate risks associated with the accelerated decision-making process?
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
