from diffusers import StableDiffusionPipeline
import torch

model_id = "/fsx/pzesheng/ck/"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

# Disable NSFW filter
def dummy(images, **kwargs):
    return images, False
pipe.safety_checker = dummy

prompt = "A,photo,of,sks,dog,in,a,bucket"
image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]

image.save("/fsx/pzesheng/repo/dog-bucket.png")