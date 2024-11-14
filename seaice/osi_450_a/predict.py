import pickle
from typing import List

import numpy as np
import torch
from PIL import Image
from netCDF4 import Dataset

from .model_factory import IceNet


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "config":  # 替换成文件中类的实际名称
            module = "seaice.osi_450_a.config"
        return super().find_class(module, name)


# 从 pkl 文件加载 configs
with open("seaice/osi_450_a/pkls/train_config_SICTeDev_update.pkl", "rb") as f:
    configs = CustomUnpickler(f).load()

model_path: str = "seaice/osi_450_a/checkpoints/checkpoint_SICTeDev_update.chk"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = IceNet(configs).to(device)
checkpoint = torch.load(model_path, map_location=device, weights_only=True)
model.load_state_dict(checkpoint["net"])
model.eval()


def predict_ice_concentration_from_images(
        image_list: List[Image.Image], input_times: List[int],
) -> np.ndarray:
    """
    从图像列表预测未来的海冰浓度。

    参数:
        image_list: 包含14个PIL图像的列表

    返回:
        np.ndarray: 预测的海冰浓度图，形状为 (12, H, W)
    """
    processed_images = []
    for img in image_list:
        if img.mode != "L":
            img = img.convert("L")
        img_array = np.array(img)
        processed_images.append(img_array)
    input_array = np.stack(processed_images)
    # 针对图片的数据预处理，除以255
    input_array = input_array / 255.0
    return _predict(input_array, input_times)


def predict_ice_concentration_from_nc_file(
        nc_file_path: str, input_times: List[int], variable_name: str = "ice_conc"
) -> np.ndarray:
    """
    从 .nc 文件预测未来的海冰浓度。

    参数：
        nc_file_path: .nc 文件的路径
        variable_name: 要读取的变量名称，默认为 'sea_ice_concentration'

    返回：
        np.ndarray: 预测的海冰浓度图，形状为 (12, H, W)
    """
    # 读取 nc 文件
    dataset = Dataset(nc_file_path)
    data = dataset.variables[variable_name][:]  # 根据实际数据结构调整索引
    dataset.close()
    # 针对 nc 文件的数据预处理，除以100
    input_array = data.astype(np.float32)
    input_array = input_array / 100.0
    return _predict(input_array, input_times)


def predict_ice_concentration_from_nc_files(
        nc_file_paths: List[str], input_times: List[int], variable_name: str = "ice_conc",
) -> np.ndarray:
    """
    从多个 .nc 文件预测未来的海冰浓度。

    参数：
        nc_file_path: .nc 文件的路径
        variable_name: 要读取的变量名称，默认为 'sea_ice_concentration'

    返回：
        np.ndarray: 预测的海冰浓度图，形状为 (12, H, W)
    """
    nc_data = []
    # 读取 nc 文件
    for nc_file_path in nc_file_paths:
        dataset = Dataset(nc_file_path)
        data = dataset.variables[variable_name][:][0]  # 根据实际数据结构调整索引
        dataset.close()
        # 针对 nc 文件的数据预处理，除以100
        input_array = data.astype(np.float32)
        input_array = input_array / 100.0
        nc_data.append(input_array)
    return _predict(np.array(nc_data), input_times)


def _predict(input_array: np.ndarray, input_times: List[int]) -> np.ndarray:
    """
    私有函数，执行实际的预测工作。

    参数:
        input_array: 经过预处理的输入数组，形状为 (12, H, W)

    返回:
        np.ndarray: 预测的海冰浓度图，形状为 (12, H, W)
    """
    # 转换为张量并调整形状
    input_tensor = torch.from_numpy(input_array)[None, :, None, :, :].float().to(device)
    input_times = torch.tensor(input_times).long().to(device)
    # 模型预测
    with torch.no_grad():
        output = model(input_tensor, input_times)

    # 转换为 numpy 数组
    prediction = output.cpu().numpy()[0]
    torch.cuda.empty_cache()
    return prediction
