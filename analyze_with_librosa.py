import pprint
import librosa
from typing import Dict, Any
import argparse
import numpy as np


class KeyDetector:
    def __init__(self):
        # Define all possible keys
        self.KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Krumhansl-Schmuckler key profiles
        self.MAJOR_PROFILE = np.array(
            [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        )
        self.MINOR_PROFILE = np.array(
            [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        )

    def detect_key(self, y: np.ndarray, sr: int) -> Dict[str, any]:
        """
        Detect the musical key and scale of an audio file

        Args:
            y (np.ndarray): Audio time series
            sr (int): Sampling rate

        Returns:
            Dict containing key, scale, and confidence scores
        """
        # Compute chromagram
        chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Average chroma features over time
        chroma_vals = np.mean(chromagram, axis=1)

        # Calculate correlation coefficients for all major and minor keys
        major_corrs = []
        minor_corrs = []

        # Test correlation with all possible keys
        for i in range(12):
            # Rotate our chroma features to match each possible key
            rotated_chroma = np.roll(chroma_vals, i)

            # Calculate correlation with major and minor profiles
            major_corr = np.corrcoef(rotated_chroma, self.MAJOR_PROFILE)[0, 1]
            minor_corr = np.corrcoef(rotated_chroma, self.MINOR_PROFILE)[0, 1]

            major_corrs.append(major_corr)
            minor_corrs.append(minor_corr)

        # Convert correlations to numpy arrays
        major_corrs = np.array(major_corrs)
        minor_corrs = np.array(minor_corrs)

        # Find best correlation for major and minor
        best_major_idx = np.argmax(major_corrs)
        best_minor_idx = np.argmax(minor_corrs)

        best_major_corr = major_corrs[best_major_idx]
        best_minor_corr = minor_corrs[best_minor_idx]

        # Determine overall key and scale
        if best_major_corr > best_minor_corr:
            key = self.KEYS[best_major_idx]
            scale = "major"
            confidence = best_major_corr
        else:
            key = self.KEYS[best_minor_idx]
            scale = "minor"
            confidence = best_minor_corr

        # Get correlation scores for the detected key in both scales
        major_conf = major_corrs[best_major_idx]
        minor_conf = minor_corrs[best_minor_idx]

        # Calculate additional confidence metrics
        scale_certainty = abs(major_conf - minor_conf) / max(
            abs(major_conf), abs(minor_conf)
        )

        return key, scale


class AudioAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Load the audio file
        self.y, self.sr = librosa.load(file_path)

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def analyze_technical_features(self) -> Dict[str, Any]:
        """Analyze technical features using librosa"""

        # Tempo estimation
        tempo, _ = librosa.beat.beat_track(y=self.y, sr=self.sr)

        # scale
        key2, scale = KeyDetector().detect_key(self.y, self.sr)

        # Calculate duration
        duration = librosa.get_duration(y=self.y, sr=self.sr)
        duration_HHMMSS = self._format_duration(duration)

        # Calculate RMS energy
        rms = librosa.feature.rms(y=self.y)[0]

        return {
            "tempo": float(tempo),
            "key": f"{key2}",
            "scale": scale,
            "rms": float(np.mean(rms)),
            "duration": duration,
            "duration_hhmmss": duration_HHMMSS,
        }
