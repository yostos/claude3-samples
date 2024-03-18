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
はい、ここでTypeScriptを使用してAWS CDKで示された構成を実装するコードの例を示します。

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

class MyInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC
    const vpc = new ec2.Vpc(this, 'MyVPC', {
      maxAzs: 3,
      natGateways: 1,
    });

    // Availability Zones
    const availabilityZones = vpc.availabilityZones;

    // Elastic Load Balancing
    const lb = new elbv2.ApplicationLoadBalancer(this, 'LB', {
      vpc,

    --- 中略 ---
}

const app = new cdk.App();
new MyInfraStack(app, 'MyInfraStack');
```


このコードでは、以下の手順を実行しています。

1. VPCを作成し、3つのアベイラビリティーゾーンとNAT Gatewayを設定しています。
2. インターネット対応のApplication Load Balancerを作成し、パブリックサブネットに配置しています。
3. 各アベイラビリティーゾーンにAmazon EC2インスタンスを作成し、プライベートサブネットに配置しています。
4. 作成したEC2インスタンスをLoad Balancerのターゲットグループに追加しています。

このコードは基本的な構成を示していますが、実際の運用環境ではさらにセキュリティグループの設定やオートスケーリンググループの作成など、追加の設定が必要になる可能性があります。

````

### translate

This will perform text translation. Even without specifying the source and target languages, it will determine the language of the input text, and properly select the source and target languages to perform the translation.

```sh
$ ./translate.py
翻訳したい文章を入力してください：Your inputs are not shared or leaked into any 3rd party and is safe for internal usage for up to highly confidential data.
入力されたデータは第三者に共有または漏洩されることなく、極秘情報を含む内部利用においても安全です。
```

### genolpqa

This will generate questions to check capabilities regarding one of the Principles of Amazon Organizational Leadership Program (OLP).

```sh
$ ./genolpqa.py
質問を生成したいOLPを番号で選択してください。
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
>> 12
Dive Deepについての質問を生成します。
```

```markdown
1. **あなたが従事していたプロジェクトで、深く探求した課題や問題点はありましたか? その際、どのように課題を掘り下げ、解決策を見つけましたか?**

   - その課題や問題点を特定するまでのプロセスを教えてください。
   - 解決策を見つける過程で、どのような困難に直面しましたか?
   - その経験から得た教訓や学びは何ですか?

2. **新しい分野や技術を習得する際、どのように深く理解しようと努力しましたか? その過程で得られた洞察や発見はありますか?**

   - 新しい知識を習得する際の具体的な学習方法は何ですか?
   - 理解を深めるために行った具体的な行動や取り組みを教えてください。
   - その経験から得られた洞察や発見はどのようなものでしたか?

3. **仕事上で複雑な問題に直面したことはありますか? その際、どのように深く掘り下げて原因を探り、解決策を見つけましたか?**

   - その問題の複雑さや難しさはどのようなものでしたか?
   - 原因を探る過程で行った具体的な行動や取り組みを教えてください。
   - その経験から得られた教訓や学びは何ですか?

4. **お客様のニーズや課題を深く理解するために、どのような取り組みを行いましたか? その過程で得られた洞察や発見はありますか?**

   - お客様のニーズや課題を理解するためにどのような方法を取りましたか?
   - その取り組みから得られた洞察や発見は何ですか?
   - その経験から学んだことは何ですか?

5. **過去の失敗や課題から学び、深く掘り下げて理解を深めた経験はありますか? その際、どのように探求し、洞察を得ましたか?**

   - その失敗や課題の内容を具体的に教えてください。
   - 深く理解するためにどのような取り組みを行いましたか?
   - その経験から得られた洞察や学びは何ですか?
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
