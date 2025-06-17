import argparse

from predictory import DeptEstimationModel


def main():
    parser = argparse.ArgumentParser(description="Depth Estimation Model CLI")
    parser.add_argument("input_image", type=str, help="Path to the input image")
    parser.add_argument("output_image", type=str, help="Path to the output depth map")
    args = parser.parse_args()

    model = DeptEstimationModel()
    result = model.calculate_depthmap(args.input_image, args.output_image)
    print(result)


if __name__ == "__main__":
    main()
