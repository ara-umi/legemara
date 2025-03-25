#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 OpenCV 实现 erolabs 滑块验证码的自动识别
"""

import cv2
import numpy as np


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
            # cv2.drawContours(approx_image, [approx], -1, (0, 255, 0), 2)  # 绘制逼近的多边形
            center = get_contour_center(approx)
            cv2.circle(approx_image, center, 5, (0, 0, 255), -1)

    cv2.imshow("approx", approx_image)
    cv2.waitKey(0)


def get_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    else:
        return None


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
