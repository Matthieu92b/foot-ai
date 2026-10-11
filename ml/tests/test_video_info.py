import importlib.util
from pathlib import Path

import cv2
import numpy as np
import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "video_info.py"
_spec = importlib.util.spec_from_file_location("video_info", _SCRIPT)
video_info = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(video_info)


@pytest.fixture
def clip(tmp_path):
    path = tmp_path / "clip.avi"
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (64, 48))
    for _ in range(20):
        writer.write(np.zeros((48, 64, 3), dtype=np.uint8))
    writer.release()
    return path


def test_get_video_info(clip):
    info = video_info.get_video_info(clip)
    assert (info.width, info.height) == (64, 48)
    assert info.fps == pytest.approx(10.0)
    assert info.frame_count == 20
    assert info.duration == pytest.approx(2.0)


def test_missing_file(tmp_path):
    with pytest.raises(video_info.VideoInfoError):
        video_info.get_video_info(tmp_path / "absent.mp4")


def test_invalid_file(tmp_path):
    bad = tmp_path / "bad.mp4"
    bad.write_text("pas une vidéo")
    with pytest.raises(video_info.VideoInfoError):
        video_info.get_video_info(bad)


def test_format_duration():
    assert video_info.format_duration(75.2) == "01:15"


def test_main_ok(clip, capsys):
    assert video_info.main([str(clip)]) == 0
    assert "64 x 48" in capsys.readouterr().out


def test_main_error_exit_code(tmp_path, capsys):
    assert video_info.main([str(tmp_path / "absent.mp4")]) != 0
    assert "introuvable" in capsys.readouterr().err
