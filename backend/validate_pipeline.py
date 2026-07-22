import os
import sys
import time
import json
import shutil
from pathlib import Path
import cv2
import numpy as np

# Set python path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.preprocessing.image_loader import ImageLoader
from app.services.perspective_service import PerspectiveService
from app.services.grayscale_service import GrayscaleService
from app.services.enhancement_service import EnhancementService
from app.services.threshold_service import ThresholdService
from app.services.table_service import TableService
from app.services.extraction_service import ExtractionService
from app.services.ocr_service import OCRService
from app.services.matching_service import MatchingService
from app.services.attendance_service import AttendanceService
from app.services.xml_service import XMLService
from app.models.image_data import ImageData
from app.visualization.table_visualizer import TableVisualizer

def main():
    print("=" * 80)
    print("SAMS COMPREHENSIVE PIPELINE VALIDATION AND DEBUGGING")
    print("=" * 80)

    # Set up absolute path for debug directory in workspace root
    workspace_root = Path("d:/4th year/2nd Sem/Computer Graphics and Visualization/Inclass/Student-Attendance-Management-Image-Processing")
    debug_dir = workspace_root / "results" / "debug"
    
    if debug_dir.exists():
        try:
            shutil.rmtree(debug_dir)
        except Exception as e:
            print(f"Warning: Could not clean debug directory: {e}")
    debug_dir.mkdir(parents=True, exist_ok=True)
    
    # Uploaded files from backend/data (simulate upload)
    image_path = ROOT / "data" / "images" / "1.jpeg"
    xml_path = ROOT / "data" / "resources" / "students.xml"
    
    print(f"Target Image: {image_path}")
    print(f"Target XML  : {xml_path}\n")
    
    # Track stage-by-stage results for final report
    report = []

    # -------------------------------------------------------------------------
    # STAGE 1: Perspective Correction
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        image_data = ImageLoader.load(image_path)
        if image_data is None or image_data.image is None:
            raise ValueError("Failed to load original image.")
        
        cv2.imwrite(str(debug_dir / "original.jpg"), image_data.image)
        
        PerspectiveService.process(image_data)
        if image_data.perspective_image is None:
            raise ValueError("Perspective image is None.")
            
        cv2.imwrite(str(debug_dir / "perspective.jpg"), image_data.perspective_image)
        
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 1: Perspective Correction",
            "status": "Success",
            "input": str(image_path.name),
            "output": "perspective.jpg",
            "dimensions": f"{image_data.perspective_image.shape[1]}x{image_data.perspective_image.shape[0]}",
            "objects_detected": 1,
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 1 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 1 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 2: Thresholding
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        GrayscaleService.process(image_data)
        EnhancementService.process(image_data)
        ThresholdService.process(image_data)
        
        thresh_img = getattr(image_data, "binary_image", None)
        if thresh_img is None:
            thresh_img = getattr(image_data, "threshold_image", None)
        if thresh_img is None:
            raise ValueError("Binary threshold image is None.")
            
        cv2.imwrite(str(debug_dir / "threshold.png"), thresh_img)
        
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 2: Thresholding",
            "status": "Success",
            "input": "perspective.jpg",
            "output": "threshold.png",
            "dimensions": f"{thresh_img.shape[1]}x{thresh_img.shape[0]}",
            "objects_detected": 1,
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 2 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 2 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 3: Table Detection
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        TableService.process(image_data)
        if image_data.table_contour is None:
            raise ValueError("No table contour detected.")
            
        table_overlay = TableVisualizer.contour(image_data)
        cv2.imwrite(str(debug_dir / "table_overlay.png"), table_overlay)
        
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 3: Table Detection",
            "status": "Success",
            "input": "threshold.png",
            "output": "table_overlay.png",
            "dimensions": f"{table_overlay.shape[1]}x{table_overlay.shape[0]}",
            "objects_detected": 1,
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 3 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 3 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 4: Grid Detection
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        grid_overlay = TableVisualizer.grid(image_data)
        cv2.imwrite(str(debug_dir / "grid_overlay.png"), grid_overlay)
        
        intersections_count = len(image_data.intersections or []) if hasattr(image_data, "intersections") else 0
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 4: Grid Detection",
            "status": "Success",
            "input": "table_overlay.png",
            "output": "grid_overlay.png",
            "dimensions": f"{grid_overlay.shape[1]}x{grid_overlay.shape[0]}",
            "objects_detected": intersections_count,
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 4 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 4 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 5: Cell Extraction & Debug Crop
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        ExtractionService.process(image_data)
        if not image_data.cells:
            raise ValueError("0 cells extracted.")
            
        cells_dir = debug_dir / "cells"
        cells_dir.mkdir(parents=True, exist_ok=True)
        
        for cell in image_data.cells:
            cell_img = cell.get("image")
            if cell_img is not None:
                cv2.imwrite(str(cells_dir / f"cell_{cell['id']:03d}.png"), cell_img)
                
        cells_overlay = image_data.perspective_image.copy()
        for cell in image_data.cells:
            x, y, w, h = cell["bbox"]
            color = (0, 255, 0) if cell.get("valid", True) else (0, 0, 255)
            cv2.rectangle(cells_overlay, (x, y), (x + w, y + h), color, 2)
        cv2.imwrite(str(debug_dir / "cells_overlay.png"), cells_overlay)
        
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 5: Cell Extraction & Validation",
            "status": "Success",
            "input": "grid_overlay.png",
            "output": f"{len(image_data.cells)} cropped images in results/debug/cells/",
            "dimensions": f"{cells_overlay.shape[1]}x{cells_overlay.shape[0]}",
            "objects_detected": f"{len(image_data.valid_cells or [])} valid / {len(image_data.cells)} total",
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 5 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 5 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 6: OCR Validation
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        OCRService.process(image_data)
        ocr_debug_list = []
        for res in (image_data.ocr_results or []):
            if res.get("column") == 1:
                ocr_debug_list.append({
                    "cell_number": res.get("id"),
                    "recognized_text": res.get("text"),
                    "confidence": res.get("confidence")
                })
        with open(debug_dir / "ocr_debug.json", "w", encoding="utf-8") as f:
            json.dump(ocr_debug_list, f, indent=2)
            
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 6: OCR Validation",
            "status": "Success",
            "input": "cells/",
            "output": "ocr_debug.json",
            "dimensions": "N/A",
            "objects_detected": len(image_data.ocr_results or []),
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 6 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 6 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 7: XML Validation
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        XMLService.process(image_data, xml_path)
        if not image_data.student_records:
            raise ValueError("No student records found in XML file.")
            
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 7: XML Validation",
            "status": "Success",
            "input": str(xml_path.name),
            "output": f"{len(image_data.student_records)} records loaded",
            "dimensions": "N/A",
            "objects_detected": len(image_data.student_records),
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 7 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 7 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 8: Matching Validation
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        MatchingService.process(image_data)
        matching_debug_list = []
        for m in (image_data.matched_students or []):
            matching_debug_list.append({
                "ocr_id": m.ocr_text,
                "matched_xml_id": m.student_id,
                "student_name": m.student_name,
                "confidence": m.confidence
            })
        with open(debug_dir / "matching_debug.json", "w", encoding="utf-8") as f:
            json.dump(matching_debug_list, f, indent=2)
            
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 8: Matching Validation",
            "status": "Success",
            "input": "ocr_results & xml_records",
            "output": "matching_debug.json",
            "dimensions": "N/A",
            "objects_detected": len(image_data.matched_students or []),
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 8 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 8 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 9: Signature Detection
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        AttendanceService.process(image_data)
        sig_overlay = image_data.perspective_image.copy()
        
        for r in (image_data.attendance_results or []):
            sig = r.get("signature")
            if sig and sig.get("bbox"):
                x, y, w, h = sig["bbox"]
                color = (0, 255, 0) if r.get("status") == "Present" else (0, 0, 255)
                cv2.rectangle(sig_overlay, (x, y), (x + w, y + h), color, 2)
        cv2.imwrite(str(debug_dir / "signature_overlay.png"), sig_overlay)
        
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 9: Signature Detection",
            "status": "Success",
            "input": "perspective.jpg",
            "output": "signature_overlay.png",
            "dimensions": f"{sig_overlay.shape[1]}x{sig_overlay.shape[0]}",
            "objects_detected": len(image_data.attendance_results or []),
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 9 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 9 failed: {e}")
        return

    # -------------------------------------------------------------------------
    # STAGE 10: Attendance Decision
    # -------------------------------------------------------------------------
    start_time = time.time()
    try:
        attendance_debug_list = []
        for r in (image_data.attendance_results or []):
            match = r.get("match")
            sig = r.get("signature")
            attendance_debug_list.append({
                "student_id": match.student_id if match else "Unknown",
                "student_name": match.student_name if match else "Unknown",
                "signature_detected": sig.get("present") if sig else False,
                "ink_ratio": sig.get("ink_ratio") if sig else 0.0,
                "attendance": r.get("status"),
                "reason": f"Ink ratio {sig.get('ink_ratio', 0.0):.4f} (contours={sig.get('contour_count', 0)}, components={sig.get('connected_components', 0)})" if sig else "No signature data"
            })
        with open(debug_dir / "attendance_debug.json", "w", encoding="utf-8") as f:
            json.dump(attendance_debug_list, f, indent=2)
            
        duration = time.time() - start_time
        report.append({
            "stage": "Stage 10: Attendance Decision",
            "status": "Success",
            "input": "signature_results",
            "output": "attendance_debug.json",
            "dimensions": "N/A",
            "objects_detected": len(image_data.attendance_results or []),
            "time": f"{duration:.3f}s"
        })
        print("[SUCCESS] Stage 10 completed.")
    except Exception as e:
        print(f"[FAILED] Stage 10 failed: {e}")
        return

    # Generate print report
    print("\n" + "=" * 80)
    print("PIPELINE VALIDATION STAGE REPORT")
    print("=" * 80)
    for row in report:
        print(f"\n- {row['stage']}: {row['status']}")
        print(f"  Input           : {row['input']}")
        print(f"  Output          : {row['output']}")
        print(f"  Dimensions      : {row['dimensions']}")
        print(f"  Objects Detected: {row['objects_detected']}")
        print(f"  Execution Time  : {row['time']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
