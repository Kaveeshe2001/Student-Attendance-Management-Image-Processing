from pathlib import Path

from sams import SAMS
from infovis import InfoVis
from investigate import Investigator


def main() -> None:
    
    # Run the complete SAMS pipeline.

    print("=" * 60)
    print("Student Attendance Management System")
    print("=" * 60)

    image_path = Path(
        "data/images/1.jpeg"
    )

    xml_path = Path(
        "data/resources/students.xml"
    )

    output_csv = Path(
        "results/final_attendance.csv"
    )

    try:

        sams = SAMS(

            image_path=image_path,

            xml_path=xml_path,

        )

        image_data = sams.run()

        print("\nProcessing completed successfully.")

        print("\nDisplaying results...")

        InfoVis.show_all(
            image_data
        )

        print("\nInvestigation Report...")

        Investigator.investigate(
            image_data
        )

        print("\nExporting CSV...")

        sams.export(
            output_csv
        )

        print(
            f"\nAttendance report saved to:\n{output_csv}"
        )

        print("\nSAMS finished successfully.")

    except Exception as error:

        print("\nProcessing failed.")

        print(error)


if __name__ == "__main__":

    main()