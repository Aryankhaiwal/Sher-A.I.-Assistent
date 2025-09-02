from diffusers import StableDiffusionPipeline
import torch

# Load the Stable Diffusion model (first time it downloads weights)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt: str, filename="generated.png"):
    try:
        image = pipe(prompt).images[0]
        image.save(filename)
        return filename
    except Exception as e:
        return f"Error generating image: {e}"
