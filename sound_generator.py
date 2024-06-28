from gradio_client import Client
import shutil
from typing import Any

import torch
import torchaudio
from einops import rearrange
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond

device = "cuda" if torch.cuda.is_available() else "cpu"

class TTAmodel:
    def __init__(self):
        self.tta, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
        self.sample_rate = model_config["sample_rate"]
        self.sample_size = model_config["sample_size"]

        self.tta = self.tta.to(device)

# Set up text and timing conditioning

    def __call__(self, prompt, seconds_total, steps, cfg_scale, api_name, output_path):
        # Set up text and timing conditioning
        conditioning = [{
            "prompt": prompt,
            "seconds_start": 0, 
            "seconds_total": seconds_total
        }]

        # Generate stereo audio
        output = generate_diffusion_cond(
            self.tta,
            steps=steps,
            cfg_scale=cfg_scale,
            conditioning=conditioning,
            sample_size=self.sample_size,
            sigma_min=0.3,
            sigma_max=500,
            sampler_type="dpmpp-3m-sde",
            device=device
        )

        # Rearrange audio batch to a single sequence
        output = rearrange(output, "b d n -> d (b n)")

        # Peak normalize, clip, convert to int16, and save to file
        output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
        torchaudio.save(output_path, output, self.sample_rate)
