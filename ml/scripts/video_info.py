"""
Affiche la durée, les fps et la résolution d'une ou plusieurs vidéos.

Usage :
    python ml/scripts/video_info.py clip.mp4
    python ml/scripts/video_info.py clip1.mp4 clip2.mp4

Note : la durée est calculée via nb_frames / fps. Elle peut être approximative
pour les vidéos à fps variable (VFR) ou certains conteneurs mal indexés.
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2


@dataclass(frozen=True)
class VideoInfo:
    path: Path
    duration: float  # secondes
    fps: float
    width: int
    height: int
    frame_count: int


class VideoInfoError(Exception):
    """Vidéo introuvable ou illisible."""


def get_video_info(path: str | Path) -> VideoInfo:
    """Lit les métadonnées d'une vidéo avec OpenCV."""
    path = Path(path)
    if not path.is_file():
        raise VideoInfoError(f"Fichier introuvable : {path}")

    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            raise VideoInfoError(f"Impossible de lire la vidéo : {path}")
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    finally:
        cap.release()

    if fps <= 0 or width <= 0 or height <= 0:
        raise VideoInfoError(f"Métadonnées vidéo invalides : {path}")

    return VideoInfo(
        path=path,
        duration=frame_count / fps,
        fps=fps,
        width=width,
        height=height,
        frame_count=frame_count,
    )


def format_duration(seconds: float) -> str:
    """Formate une durée en secondes au format mm:ss."""
    total = round(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def format_info(info: VideoInfo) -> str:
    return (
        f"{info.path}\n"
        f"  Durée      : {info.duration:.2f} s ({format_duration(info.duration)})\n"
        f"  FPS        : {info.fps:.2f}\n"
        f"  Résolution : {info.width} x {info.height}\n"
        f"  Frames     : {info.frame_count}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Affiche la durée, les fps et la résolution de vidéos. "
        "La durée (nb_frames / fps) peut être approximative pour les vidéos à fps variable."
    )
    parser.add_argument("videos", nargs="+", help="chemin(s) de vidéo")
    args = parser.parse_args(argv)

    exit_code = 0
    for video in args.videos:
        try:
            print(format_info(get_video_info(video)))
        except VideoInfoError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
