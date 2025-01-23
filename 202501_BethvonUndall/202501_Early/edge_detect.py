## EDGE DETECTION SCRIPT
## Running base conda venv
import cv2
import numpy as np
from pathlib import Path
import concurrent.futures
import logging
from tqdm import tqdm
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_gpu():
    """Check if GPU is available"""
    if cv2.cuda.getCudaEnabledDeviceCount():
        logger.info(f"Found {cv2.cuda.getCudaEnabledDeviceCount()} CUDA device(s)")
        return True
    logger.info("No CUDA devices found, using CPU")
    return False

def setup_directories(input_dir: str, output_dir: str) -> tuple[Path, Path]:
    """Create input and output directories if they don't exist."""
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return in_dir, out_dir

def process_frame_gpu(args) -> None:
    """Process a single frame with edge detection using GPU."""
    input_path, output_path = args
    try:
        # Read image
        frame = cv2.imread(str(input_path))
        if frame is None:
            logger.error(f"Failed to read frame: {input_path}")
            return
        
        gpu_frame = cv2.cuda_GpuMat()
        gpu_frame.upload(frame)
        
        # Convert to Grayscale on GPU
        gpu_gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur on GPU
        gpu_blurred = cv2.cuda.GaussianBlur(gpu_gray, (3, 3), 0) # Reduce blur for more detail.
        
        # Create GPU Canny detector
        detector = cv2.cuda.createCannyEdgeDetector(
            low_thresh=30,    # Adjust these thresholds - lower for more detail
            high_thresh=250   # based on your needs
        )
    
        # Apply Canny edge detection on GPU
        gpu_edges = detector.detect(gpu_blurred)
        
        # Download result from GPU
        edges = gpu_edges.download()
        
        # Save the processed frame
        cv2.imwrite(str(output_path), edges)
        
    except Exception as e:
        logger.error(f"Error processing {input_path}: {str(e)}")
        
def process_frame_cpu(args) -> None:
    """Process a single frame with edge detection using CPU."""
    input_path, output_path = args
    try:
        # Read image
        frame = cv2.imread(str(input_path))
        if frame is None:
            logger.error(f"Failed to read frame: {input_path}")
            return
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (1, 1), 0) # Reduce the blur for more detail
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred,             # I put gray in there to avoid using blurred
                          threshold1=5,    # Adjust these thresholds - lower for more detail
                          threshold2=50)   # based on your needs.
        
        cv2.imwrite(str(output_path), edges)
        
    except Exception as e:
        logger.error(f"Error processing {input_path}: {str(e)}")
        
def process_batch(input_dir: str, output_dir: str, num_workers: int = None) -> None:
    """Process a batch of frames using parallel processing."""
    in_dir, out_dir = setup_directories(input_dir, output_dir)
    
    # Check for GPU support
    use_gpu = check_gpu() # Returns True or False
    process_func = process_frame_gpu if use_gpu else process_frame_cpu # use_gpu has value True or False
    
    # Get list of all frames
    frame_files = sorted(in_dir.glob('*.png'))
    
    if not frame_files:
        frame_files = sorted(in_dir.glob('*.jpg'))
    
    if not frame_files:
        logger.error(f"No frames found in {input_dir}")
        return
    
    # Create output paths
    out_paths = [out_dir / f"{frame.stem}{frame.suffix}" for frame in frame_files]

    # Create processing pairs
    process_args = list(zip(frame_files, out_paths))
    
    # For GPU processing, we might want fewer works
    if use_gpu:
        num_workers = min(num_workers or 2, 2) # Limit to 2 workers for GPU
        
    # Process frames in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        list(tqdm(executor.map(process_func, process_args),
                  total=len(process_args),
                  desc="Processing frames"))

if __name__ == "__main__":              # Python convention to make sure scripts are not run when imported as modules, but only as standalone scripts.
    INPUT_DIR = "raw_frames_2"          # Input folder
    OUTPUT_DIR = "processed_frames_2"   # Output folder
    
    # Use number of CPU cores minus 1 to avoid system lockup
    # If using GPU, this will be limited to 2 in the process_batch functino
    NUM_WORKERS = max(1, os.cpu_count() - 1)
    
    process_batch(INPUT_DIR, OUTPUT_DIR, NUM_WORKERS)
    logger.info("Batch processing complete!")
    
    
        