# -*- coding: utf-8 -*-
from pathlib import Path

def getProjectRootPath() -> Path:
    """
    현재 프로젝트의 최상위 경로(절대경로)를 가져옴
    """
    return Path(__file__).parent.parent

def getFrameImagePath(path: str) -> Path:
    """
    현재 프로젝트의 frame에 사용되는 이미지 폴더 경로
    """
    return getProjectRootPath() / r"images" / Path(path)

def getFrameUtilPath(path: str) -> Path:
    """
    현재 프로젝트의 frame에 사용되는 이미지 폴더 경로
    """
    return getProjectRootPath() / r"utils" / Path(path)