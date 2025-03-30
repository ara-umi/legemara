#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 OpenCV 实现 erolabs 滑块验证码的自动识别
"""

from typing import Optional

import cv2
import numpy as np


def _get_contour_center(contour) -> Optional[tuple[int, int]]:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    else:
        return None


def process_erolabs_slider(
        image: np.ndarray,
) -> int:
    """
    处理 erolabs 黑端验证码
    传入不包含开始位置的验证码截图，返回需要拖动的 x 距离（包含补正）
    检测不出来的情况下会返回 0
    这个是真要严格基于 1600 x 900 的分辨率了，其他分辨率下基本上不能用（我没测过）
    """
    # 将图像转换为 HSV 颜色空间（更适合颜色筛选）
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义浅灰色的 HSV 范围
    lower_gray = np.array([0, 0, 150])  # 灰白色下限
    upper_gray = np.array([180, 50, 255])  # 灰白色上限

    # 创建掩码（提取浅灰色区域）
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # 将浅灰色区域提取出来并高光
    target = cv2.bitwise_and(image, image, mask=mask)
    non_target = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    highlighted = cv2.addWeighted(target, 0.8, non_target, 0.2, 100)

    # 灰度化
    gray = cv2.cvtColor(highlighted, cv2.COLOR_BGR2GRAY)

    # 提高对比度
    equalize = cv2.equalizeHist(gray)

    # 二值化
    ret, binary = cv2.threshold(equalize, 240, 255, cv2.THRESH_BINARY)

    # 轮廓检测
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 面积检测
    x = 0
    area_delta: float = np.inf
    for contour in contours:
        area = cv2.contourArea(contour)

        # 统一都是两个凸包一个凹包
        area_square = 65 * 65  # 标准正方形的面积
        area_round = 3.14 * 15 * 15  # 凹凸圆形的面积（完整）
        area_base = area_square + area_round * 0.9  # 因为不完整所以乘以了 0.9
        # 理论上检测出来面积只会更大，不太可能更小
        if area_base + 2 * area_round > area > area_base - 2 * area_round:  # 用圆形面积当允许误差的基准但我
            peri = cv2.arcLength(contour, True)  # 计算轮廓周长, True 表示闭合
            approx = cv2.approxPolyDP(contour, 0.01 * peri, True)  # 多边形逼近
            center = _get_contour_center(approx)
            if center:
                # 这里算检测成功了，但可能有多个检测结果（如果效果好的话一般都只有一个）
                # 多个的情况下很麻烦，只能说你越贴近这个面积你越准
                this_area_delta = abs(area - area_base)
                if this_area_delta < area_delta:
                    area_delta = this_area_delta
                    x = center[0]

    if x:
        # 补正
        # 这个补正本身是要加上开始位置
        # 另一方面还要补正是，由于多边形总是右凸，测出的中心点总是会偏右
        # 还有一方面是滑条有滞后性，一开始拖动一定距离它会不动，反正有误差
        correction_x = 76
        x += correction_x

    return x


"""
下面是面条测试代码
"""


def one(
        image
):
    # cv2.imshow("Slider", image)
    # cv2.waitKey(0)

    # 将图像转换为 HSV 颜色空间（更适合颜色筛选）
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义浅灰色的 HSV 范围
    lower_gray = np.array([0, 0, 150])  # 灰白色下限
    upper_gray = np.array([180, 50, 255])  # 灰白色上限

    # 创建掩码（提取浅灰色区域）
    mask = cv2.inRange(hsv, lower_gray, upper_gray)
    # cv2.imshow("Mask", mask)
    # cv2.waitKey(0)

    # 将浅灰色区域提取出来
    target = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imshow("Target", target)
    # cv2.waitKey(0)

    non_target = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    # cv2.imshow("Non-Target", non_target)
    # cv2.waitKey(0)

    highlighted = cv2.addWeighted(target, 0.8, non_target, 0.2, 100)
    # cv2.imshow('Highlighted', highlighted)
    # cv2.waitKey(0)

    # 灰度化
    gray = cv2.cvtColor(highlighted, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray Image", gray)
    # cv2.waitKey(0)

    # 提高对比度
    equalize = cv2.equalizeHist(gray)
    # cv2.imshow("equalize Image", equalize)
    # cv2.waitKey(0)

    # 二值化
    ret, binary = cv2.threshold(equalize, 240, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Binary Image", binary)
    # cv2.waitKey(0)

    # 轮廓检测
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 在原始图像上绘制轮廓
    contour_image = image.copy()  # 复制原始图像
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)  # 绘制所有轮廓

    # 显示带轮廓的图像
    cv2.imshow("Contours", contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 面积检测
    approx_image = image.copy()
    for contour in contours:
        area = cv2.contourArea(contour)

        # 统一都是两个凸包一个凹包
        # 所以基准就是 area_threshold + (2 - 1) * area_shift
        area_threshold = 65 * 65
        area_shift = 24 * 24
        if area_threshold + 3 * area_shift > area > area_threshold - area_shift:
            peri = cv2.arcLength(contour, True)  # 计算轮廓周长, True 表示闭合
            approx = cv2.approxPolyDP(contour, 0.01 * peri, True)  # 多边形逼近
            cv2.drawContours(approx_image, [approx], -1, (0, 255, 0), 2)  # 绘制逼近的多边形
            center = _get_contour_center(approx)
            cv2.circle(approx_image, center, 5, (0, 0, 255), -1)

    cv2.imshow("approx", approx_image)
    cv2.waitKey(0)


def test():
    for i in range(10):
        path = f"../images/slider/slider{i}.png"
        slider = cv2.imread(path, 1)
        if slider is None:
            continue
        one(slider)
        # break


if __name__ == "__main__":
    test()
