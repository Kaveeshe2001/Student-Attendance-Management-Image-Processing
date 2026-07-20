from __future__ import annotations

import matplotlib.pyplot as plt

from app.models.image_data import ImageData
from app.matching.match_result import MatchResult
from app.utils.exceptions import ImageProcessingError


class MatchingVisualizer:
    
    # Visualize student matching results.

    @staticmethod
    def show(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Display a single matched student.

        matches = image_data.matched_students

        if not matches:

            raise ImageProcessingError(
                "No matching results available."
            )

        if index < 0 or index >= len(matches):

            raise IndexError(
                "Match index out of range."
            )

        match: MatchResult = matches[index]

        plt.figure(figsize=(7, 4))
        plt.axis("off")

        plt.title(
            "Student Match",
            fontsize=15,
            fontweight="bold",
        )

        lines = [

            f"Student ID      : {match.student_id}",

            f"Student Name    : {match.student_name}",

            f"OCR Text        : {match.ocr_text}",

            f"Cleaned Text    : {match.cleaned_text}",

            f"Row             : {match.row}",

            f"Column          : {match.column}",

            f"Match Type      : {match.match_type}",

            f"Match Score     : {match.match_score:.2f}%",

            f"OCR Confidence  : {match.confidence:.2f}%",

            f"Review Required : {match.requires_review}",

        ]

        plt.text(

            0.02,

            0.98,

            "\n".join(lines),

            fontsize=11,

            va="top",

            family="monospace",

        )

        plt.tight_layout()

        plt.show()

    @staticmethod
    def list_matches(
        image_data: ImageData,
    ) -> None:
        
        # Print all matched students.

        matches = image_data.matched_students

        if not matches:

            raise ImageProcessingError(
                "No matching results available."
            )

        print()

        print("=" * 90)

        print("MATCHED STUDENTS")

        print("=" * 90)

        for i, match in enumerate(matches, start=1):

            print(

                f"{i:3d}. "

                f"{match.student_id:<12}"

                f"{match.student_name:<30}"

                f"{match.match_type:<15}"

                f"{match.match_score:6.2f}%"

            )

        print("=" * 90)

    @staticmethod
    def review_required(
        image_data: ImageData,
    ) -> None:
        
        # Print matches requiring manual review.

        matches = image_data.matched_students

        if not matches:

            raise ImageProcessingError(
                "No matching results available."
            )

        review = [

            m

            for m in matches

            if m.requires_review

        ]

        print()

        print("=" * 80)

        print("MANUAL REVIEW")

        print("=" * 80)

        if not review:

            print("No manual review required.")

            return

        for match in review:

            print(

                f"{match.student_id:<12}"

                f"{match.student_name:<30}"

                f"{match.match_score:6.2f}%"

            )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> None:
        
        # Print matching statistics.

        stats = image_data.matching_statistics

        if not stats:

            print("No statistics available.")

            return

        print()

        print("=" * 60)

        print("MATCHING STATISTICS")

        print("=" * 60)

        for key, value in stats.items():

            print(f"{key:<30}: {value}")

        print("=" * 60)

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Print a concise summary.

        matches = len(image_data.matched_students or [])

        unmatched = len(image_data.unmatched_results or [])

        print()

        print("Matching Summary")

        print("------------------------------")

        print(f"Matched Students : {matches}")

        print(f"Unmatched OCR    : {unmatched}")

        print("------------------------------")