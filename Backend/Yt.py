import yt_dlp
import os
import time

def update_file_timestamp(file_path):
    """ Update the modified date of the file to the current time """
    current_time = time.time()
    try:
        os.utime(file_path, (current_time, current_time))  # Update access & modified times
    except Exception as e:
        print(f"⚠️ Could not update modified date: {e}")

def download_youtube():
    url = input("Enter YouTube video URL: ").strip()

    # Ask user for filename preference
    use_custom_name = input("\nDo you want to use a custom file name? (yes/no): ").strip().lower()
    custom_name = ""

    if use_custom_name in ["yes", "y"]:
        custom_name = input("Enter custom file name (without extension): ").strip()

    print("\nChoose download format:")
    print("1: MP3 (Audio Only)")
    print("2: MP4 (Video Only)")
    print("3: Both MP3 & MP4")
    choice = input("Enter your choice (1/2/3): ").strip()

    # Define file save paths
    base_mp3_path = "D:/Downloads/YT MP3 Downloads/"
    base_mp4_path = "D:/Downloads/YT MP4 Downloads/"

    # Determine filename template
    if custom_name:
        filename_template = custom_name + ".%(ext)s"
    else:
        filename_template = "%(title)s.%(ext)s"  # Default to video title

    downloaded_files = []  # To store file paths for timestamp update

    if choice in ["1", "3"]:  # Download MP3
        mp3_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(base_mp3_path, filename_template),
            'no-mtime': True,  # Prevents using YouTube's upload date
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        print("\nDownloading MP3...")
        try:
            with yt_dlp.YoutubeDL(mp3_opts) as ydl:
                ydl.download([url])
            downloaded_files.append(os.path.join(base_mp3_path, filename_template.replace("%(ext)s", "mp3")))
            print(f"✅ MP3 saved to: {base_mp3_path}")
        except Exception as e:
            print(f"❌ Error downloading MP3: {e}")

    if choice in ["2", "3"]:  # Download MP4
        mp4_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(base_mp4_path, filename_template),
            'no-mtime': True,  # Prevents using YouTube's upload date
            'merge_output_format': 'mp4',
        }
        print("\nDownloading MP4...")
        try:
            with yt_dlp.YoutubeDL(mp4_opts) as ydl:
                ydl.download([url])
            downloaded_files.append(os.path.join(base_mp4_path, filename_template.replace("%(ext)s", "mp4")))
            print(f"✅ MP4 saved to: {base_mp4_path}")
        except Exception as e:
            print(f"❌ Error downloading MP4: {e}")

    if choice not in ["1", "2", "3"]:
        print("❌ Invalid choice! Please enter 1, 2, or 3.")
    
    # Update modified date of downloaded files
    for file_path in downloaded_files:
        if os.path.exists(file_path):
            update_file_timestamp(file_path)

# Run the function
download_youtube()
