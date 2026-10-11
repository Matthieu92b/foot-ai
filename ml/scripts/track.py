"""
Étape 1 — Détection + tracking des joueurs et du ballon.

Usage :
    pip install ultralytics supervision
    python track.py --source match.mp4

Sorties :
    output.mp4  -> vidéo annotée (ellipse + ID sous chaque joueur, triangle sur le ballon)
    tracks.csv  -> positions frame par frame (servira pour la projection 2D et les stats)
"""
import argparse
import csv

import numpy as np
import supervision as sv
from ultralytics import YOLO

PERSON, BALL = 0, 32  # classes COCO


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True, help="chemin de la vidéo")
    p.add_argument("--output", default="output.mp4")
    p.add_argument("--csv", default="tracks.csv")
    p.add_argument("--model", default="yolo11m.pt", help="yolo11n.pt si pas de GPU")
    p.add_argument("--conf", type=float, default=0.3)
    args = p.parse_args()

    model = YOLO(args.model)
    info = sv.VideoInfo.from_video_path(args.source)

    ellipse = sv.EllipseAnnotator(thickness=2)
    label = sv.LabelAnnotator(text_position=sv.Position.BOTTOM_CENTER, text_scale=0.4)
    triangle = sv.TriangleAnnotator(color=sv.Color.from_hex("#FFD700"), base=20, height=17)

    results = model.track(
        source=args.source,
        stream=True,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[PERSON, BALL],
        conf=args.conf,
        verbose=False,
    )

    with sv.VideoSink(args.output, info) as sink, open(args.csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "track_id", "class", "x", "y", "conf"])

        for i, r in enumerate(results):
            frame = r.orig_img.copy()
            det = sv.Detections.from_ultralytics(r)

            # --- Joueurs ---
            players = det[det.class_id == PERSON]
            if len(players) and players.tracker_id is not None:
                labels = [f"#{t}" for t in players.tracker_id]
                frame = ellipse.annotate(frame, players)
                frame = label.annotate(frame, players, labels)
                # point au sol = bas de la bbox (utile pour l'homographie plus tard)
                feet = players.get_anchors_coordinates(sv.Position.BOTTOM_CENTER)
                for t, (x, y), c in zip(players.tracker_id, feet, players.confidence):
                    writer.writerow([i, int(t), "player", round(float(x), 1), round(float(y), 1), round(float(c), 3)])

            # --- Ballon : on garde la détection la plus sûre ---
            ball = det[det.class_id == BALL]
            if len(ball):
                ball = ball[np.array([int(ball.confidence.argmax())])]
                frame = triangle.annotate(frame, ball)
                (x, y), = ball.get_anchors_coordinates(sv.Position.CENTER)
                writer.writerow([i, -1, "ball", round(float(x), 1), round(float(y), 1), round(float(ball.confidence[0]), 3)])

            sink.write_frame(frame)
            if i % 50 == 0:
                print(f"frame {i}/{info.total_frames}")

    print(f"OK -> {args.output} + {args.csv}")


if __name__ == "__main__":
    main()
