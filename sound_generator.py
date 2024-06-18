from gradio_client import Client
import shutil
from typing import Any

        
class TTAmodel:
    def __init__(self):
        self.tta = Client("artificialguybr/Stable-Audio-Open-Zero")

    def __call__(self, prompt, seconds_total, steps, cfg_scale, api_name, output_path):
        result = self.predict(prompt=prompt,	seconds_total=seconds_total, steps=steps, cfg_scale=cfg_scale, api_name=api_name)
        shutil.copyfile(result, output_path)
        print('Done.')


tta = Client("artificialguybr/Stable-Audio-Open-Zero")
result = tta.predict(
		prompt="Generate an energetic and bustling city street scene with distant traffic and close conversations.",
		seconds_total=15,
		steps=100,
		cfg_scale=10,
		api_name="/predict"
)

shutil.copyfile(result, './audio3.wav')
print('Done.')