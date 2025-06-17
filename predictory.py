import torch
from misc import colorize
from PIL import Image


class DeptEstimationModel:
    def __init__(self) -> None:
        self.device = self._get_device()
        self.model = self._initialize_model(
            model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"
        ).to(self.device)

    def _get_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _initialize_model(self, model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"):
        torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=True)
        model = torch.hub.load(
            model_repo, model_name, pretrained=True, skip_validation=True
        )
        model.eval()
        print("Model initialized.")
        return model

    def save_color_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        Image.fromarray(colored).save(output_path)
        print(f"Colorized depth map saved to {output_path}")

    def calculate_depthmap(self, image_path, output_path):
        image = Image.open(image_path).convert("RGB")
        print(f"Processing image: {image_path}")
        depth_numpy = self.model.infer_pil(image)
        self.save_color_depth(depth_numpy, output_path)
        return f"Depth map saved to {output_path}"


model = DeptEstimationModel()
model.calculate_depthmap("./test_image.png", "output_image.png")
