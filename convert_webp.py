import os
from PIL import Image, ImageSequence

# Define the target size
TARGET_SIZE = (500, 280)
PROCESSED_FOLDER = "processed"

def resize_animated_image(input_path, output_path, size):
    """
    Resize an animated image to the given size, maintaining aspect ratio,
    and save it as an animated .webp file.
    """
    with Image.open(input_path) as img:
        frames = []

        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")  # Ensure compatibility

            # Calculate aspect ratio
            img_ratio = frame.width / frame.height
            target_ratio = size[0] / size[1]

            if img_ratio > target_ratio:
                # Image is wider than target; crop width
                new_height = size[1]
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller than target; crop height
                new_width = size[0]
                new_height = int(new_width / img_ratio)

            resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Center crop to target size
            left = (resized_frame.width - size[0]) / 2
            top = (resized_frame.height - size[1]) / 2
            right = (resized_frame.width + size[0]) / 2
            bottom = (resized_frame.height + size[1]) / 2
            cropped_frame = resized_frame.crop((left, top, right, bottom))

            frames.append(cropped_frame)

        # Save as animated WEBP
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=img.info.get("duration", 100),
            loop=img.info.get("loop", 0),
            format="WEBP"
        )

def process_images():
    """
    Process all .webp and .gif images in the current directory.
    Resized images are saved in the 'processed' subfolder.
    """
    # Create the processed folder if it doesn't exist
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    # Get the list of files in the current directory
    for file_name in os.listdir("."):
        if file_name.lower().endswith((".webp", ".gif")):
            input_path = file_name
            output_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file_name)[0]}.webp")
            try:
                resize_animated_image(input_path, output_path, TARGET_SIZE)
                print(f"Processed: {file_name} -> {output_path}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    process_images()
