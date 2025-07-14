# Amazon Bedrock nodes for ComfyUI


[***Amazon Bedrock***](https://aws.amazon.com/bedrock/) is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies.
This repo is the ComfyUI nodes for Bedrock service. You can invoke foundation models in your ComfyUI pipeline.

## Installation (SageMaker by CloudFormation)

Using [__*Amazon SageMaker*__](https://aws.amazon.com/sagemaker/) is the easiest way to develop your AI model. You can deploy a ComfyUI on SageMaker notebook using CloudFormation.

1. Open [CloudFormation console](https://console.aws.amazon.com/cloudformation/home#/stacks/create), and upload [`./assets/comfyui_on_sagemaker.yaml`](https://raw.githubusercontent.com/aws-samples/comfyui-llm-node-for-amazon-bedrock/main/assets/comfyui_on_sagemaker.yaml) by "Upload a template file".
2. Next enter a stack name, choose a instance type fits for you.  Just next and next and submit.
3. Wait for a moment, and you will find the ComfyUI url is ready for you. Enjoy!

![](./assets/stack_complete.webp)

## Installation (Manually)

1. Clone this repository to your ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aws-samples/comfyui-llm-node-for-amazon-bedrock.git
pip install -r comfyui-llm-node-for-amazon-bedrock/requirements.txt

# better to work with some third-party nodes
git clone https://github.com/WASasquatch/was-node-suite-comfyui.git
git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git
```

2. You need to make sure your access to Bedrock models are granted. Go to aws console [*https://console.aws.amazon.com/bedrock/home#/modelaccess*](https://console.aws.amazon.com/bedrock/home#/modelaccess) . Make sure these models in the figure are checked.

![](./assets/base_models_us-east-1.png)
![](./assets/base_models_us-east-2.png)


3. You need to configure credentials for your environment. There are several options:

### Option 1: Config.ini File (Easy)

Create a `config.ini` file in the custom_nodes directory with your AWS credentials:

```ini
[aws]
access_key_id = YOUR_ACCESS_KEY_ID
secret_access_key = YOUR_SECRET_ACCESS_KEY
region = us-east-1
```

You can copy `config.ini.example` and edit it with your actual credentials.

### Option 2: IAM Role (AWS Instances)

If you are running ComfyUI on an AWS instance, you can use IAM role to control the policy to access to Bedrock service without credential configuration.

Open the IAM role console of your running instance, and attach `AmazonBedrockFullAccess` policy to your role.

Alternatively, you can create an inline policy to your role like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:*",
            "Resource": "*"
        }
    ]
}
```

### Option 3: AWS CLI Credentials

You can use the aws command tool to configure your credentials file:

```
aws configure
```

Alternatively, you can create the credentials file yourself. By default, its location is ~/.aws/credentials. At a minimum, the credentials file should specify the access key and secret access key. In this example, the key and secret key for the account are specified in the default profile:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

You may also want to add a default region to the AWS configuration file, which is located by default at ~/.aws/config:

```
[default]
region=us-east-1
```

If you haven't set the default region and running on aws instance, this nodes will automatically use the same region as the running instance.

## Example

Workflow examples are in `./workflows`. To import these workflows, click "Load" in the ComfyUI UI, go to workflows directory and choose the one you want to experiment with.

### Text to image with prompt translation and refinement
Automatically refine the text prompt to generate high quality images.

Download [this workflow file](workflows/text2img_with_prompt_refinement.json) and load in ComfyUI

You can use the Bedrock LLM to refine and translate the prompt. It then utilize the image generation model (eg. SDXL, Titan Image) provided by Bedrock.
The result is much better after preprocessing of prompt compared to the original SDXL model (the bottom output in figure) which doesn't have the capability of understanding Chinese.

![](./assets/example_prompts_refine.webp)

### Image Caption with Claude 3

Generate captions of a provided image.

Download [this workflow file](workflows/claude3_image_caption.json) and load in ComfyUI

This workflow uses Bedrock Claude 3 multimodal to caption image.

![](./assets/example_claude3_multimodal.webp)

### Inpainting with natural language
Use natural language to describe an item in the image and replace it. 

Download [this workflow file](workflows/inpainting_with_natural_language.json) and load in ComfyUI

This workflow leverages Claude3 to analyze the replacement information in the prompt. Additionally, it utilizes Bedrock Titan Image to detect objects with text and perform inpainting in a single step.

![](./assets/example_inpainting_with_natural_language.webp)

### Generate Image Variation
Use natural language to generate variation of an image.

Download [this workflow file](workflows/generate_image_variation.json) and load in ComfyUI

This workflow begins by using Bedrock Claude3 to refine the image editing prompt. It then utilizes Bedrock Titan Image's variation feature to generate similar images based on the refined prompt.

![](./assets/example_generate_image_variation.webp)


### Generate Image Variation with Image Caption
Use natural language to generate variation of an image without re-describing the original image content.

Download [this workflow file](workflows/variation_with_caption.json) and load in ComfyUI

This workflow begins by using Bedrock Claude3 to refine the image editing prompt, generation caption of the original image, and merge the two image description into one. It then utilizes Bedrock Titan Image's variation feature to generate similar images based on the refined prompt.

![](./assets/example_variation_with_caption.webp)

### Nova Canvas Examples
Generate stunning images using Amazon's Nova Canvas model, supporting following capabilities:
- text-to-image including color-palette support and reference image for style reference
- image-to-image for generating variations
- image-to-image for background replacement

You'll find all nodes in [this workflow file](workflows/amazon_nova_canvas_nodes.json) or download the png below and drag'n'drop it into ComfyUI 

This workflows showcases all available Amazon Nova Canvas Nodes.
![](./assets/nova_canvas_workflows.png)
  

### Text to Video with Amazon Nova Reel
Generate engaging videos using Amazon's Nova Reel model, supporting both text-to-video and image-to-video generation.

Text-to-Video Workflow: Download [this workflow file](workflows/text2vid_nova_reel.json) or the png below and load in ComfyUI  
Image-to-Video Workflow: Download [this workflow file](workflows/img2vid_nova_reel.json) or the png below and load in ComfyUI

This workflows showcases Amazon Nova Reel's capabilities to transform text descriptions or images into dynamic video content.

![](./assets/text2vid_nova_reel.png)
![](./assets/img2vid_nova_reel.png)

The workflow combines:
- Nova Reel's text-to-video and image-to-video generation
- Use dimension 1280x720
- Controls for seed and have the option to control_after_generate
- Support for S3 bucket destination configuration

Example output:  
https://github.com/aws-samples/comfyui-llm-node-for-amazon-bedrock/tree/main/assets/text2vid_nova_reel_output_example.mp4  
https://github.com/aws-samples/comfyui-llm-node-for-amazon-bedrock/tree/main/assets/img2vid_nova_reel_output_example.mp4  


### Text to Video with Luma Ray
Generate high-quality videos from text descriptions using Luma AI's Ray model.

Download [this workflow file](workflows/text2vid_luma_ray2.json) or the png below and load in ComfyUI

This workflow demonstrates how to use Luma AI's Ray model through Bedrock to create dynamic videos from text prompts.

![](./assets/text2vid_luma_ray.png)

The workflow combines:
- Luma Ray's advanced text-to-video capabilities
- Options to control aspect-ratio, resolution, video duration, destination_bucket, and loop option

Example output:  
https://github.com/aws-samples/comfyui-llm-node-for-amazon-bedrock/tree/main/assets/text2vid_luma_output_example.mp4

### Stability AI Models Nodes
Generate stunning images using Stability AIs most recent models, supporting following capabilities:
- text-to-image
  - SD3 Large
  - SD3.5 Large
  - Stable Image Ultra
  - Stable Image Core
- image-to-image for generating variations
  - SD3 & SD3.5 Large

You'll find all nodes in [this workflow file](workflows/amazon_stablity_ai.json) or download the png below and drag'n'drop it into ComfyUI 

This workflows showcases all available Amazon Nova Canvas Nodes.
![](./assets/stability_ai_workflows.png)  

## Supported models

Here are models ready for use, more models are coming soon.

- Luma:
  - [X] Ray2

- Anthropic:
  - [X] Claude (1.x, 2.0, 2.1, haiku, sonnet, opus)
  - [X] Claude Instant (1.x)

- Amazon:
  - Nova LLM
    - [X] Nova Lite
    - [X] Nova Pro
  
  - Nova Canvas
    - [X] text to image
    - [ ] inpainting
    - [ ] outpainting
    - [X] image variation
    - [ ] image conditioning
    - [X] background replacement (with prompt)
  
  - Nova Reel
    - [X] text to video
    - [X] image to video

  - Titan Image Generator G1 (1.x)
    - [X] text to image
    - [X] inpainting
    - [X] outpainting
    - [X] image variation

  
- Stability AI:
  - Stable Diffusion XL (1.0)
    - [X] text to image
    - [ ] image to image
    - [ ] image to image (masking)
  - SD3 Large (1.0)
    - [X] text to image
    - [X] image to image
  - SD3.5 Large (1.0)
    - [X] text to image
    - [X] image to image
  - Stable Diffusion Image Core (v1.1)
    - [X] text to image
  - Stable Diffusion Image Ultra (v1.1)
    - [X] text to image

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

