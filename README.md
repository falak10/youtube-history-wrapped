# YouTube Wrapped Dashboard

A local, privacy-first analytics dashboard that visualizes your entire YouTube watch history. Built with Python and Streamlit.

Since YouTube (unlike Spotify) doesn't provide a detailed year-end wrap-up on demand, this tool parses your personal Google Takeout data to generate insights, top channels, activity heatmaps, and more.

---

## Features

* Yearly Filtering: Switch instantly between your 2025 stats, 2024, or All-Time history.
* Activity Heatmaps: Visualize exactly when you watch (Day of Week vs. Hour of Day).
* Top Channels: See who you watched the most.
* Monthly Activity: Track your viewing habits throughout the year.
* Privacy Focused: Runs 100% locally on your machine. Your data never leaves your computer.

---

## How the Metrics Work

### 1. The Time Estimate
Google's export file (watch-history.html) is a log of clicks, not a log of duration.
* What Google provides: "User clicked Video X at 4:00 PM."
* What is missing: "User stopped watching at 4:05 PM."

Because the file contains no data on how long you actually stayed on a video, exact watch time is impossible to calculate without querying the YouTube API for every single link.
* Our Solution: The dashboard assumes an average watch time of 10 minutes per video to calculate "Estimated Hours."

### 2. Total Views vs. Unique Videos
The dashboard includes a toggle to switch between two different ranking logics:

* Total Views (Includes Re-watches): Counts every single click. Best for identifying your "comfort shows" or music videos you play on repeat.
* Unique Videos (Ignores Re-watches): Removes duplicates based on the Video Title and Channel. Best for seeing how many distinct videos you discovered.

---

## Step 1: Get Your Data (Google Takeout)

You need to export your history from Google. This usually takes a few minutes.

1. Go to Google Takeout (takeout.google.com).
2. Click "Deselect All".
3. Scroll down to find "YouTube and YouTube Music" and check the box.
4. Click on the button that says "All YouTube data included".
   * Uncheck everything except "history".
   * Click OK.
5. Click on "Multiple Formats".
   * Ensure "History" is set to HTML.
   * Click OK.
6. Scroll to the bottom and click "Next Step".
7. Select "Export once" and click "Create Export".
8. Check your email. Download the zip file, extract it, and look for the file named "watch-history.html".
9. Move "watch-history.html" into the same folder as this script.

---

## Step 2: Installation & Usage

### Prerequisites
You need Python installed on your system.

### Installation
1. Clone this repository or download the files.
2. Open your terminal/command prompt in the project folder.
3. Install the required dependencies:

pip install -r requirements.txt

### Running the App
Execute the following command in your terminal:

streamlit run app.py

A browser tab should open automatically at http://localhost:8501 displaying your stats.

---


## License

This project is open-source. Feel free to modify and use it to analyze your own data!
