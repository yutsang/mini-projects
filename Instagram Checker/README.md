# Instagram Follower Comparison Tool
This Python script analyzes Instagram following and follower data from HTML files, comparing the lists to identify users you follow who don't follow you back, and users who follow you but you don't follow.

## Features
- Parses Instagram HTML files for usernames and dates
- Compares following and follower lists
- Outputs results to a CSV file

## Requirements
Python 3.x, BeautifulSoup4, pandas

##Installation
1. Clone this repository or download the script.
2. Install the required packages:
```
pip install beautifulsoup4 pandas
```

## Usage
1. Place your Instagram data files in the following directory structure:
```
./connections/followers_and_following/
├── following.html
└── followers_1.html
```

2. Run the script:
```
python instagram_follower_comparison.py
```

3. The script will generate an ig_comparison.csv file in the current directory, containing two columns:
"Following Only": Users you follow who don't follow you back
"Followers Only": Users who follow you but you don't follow

## Customization
You can modify the instagram_data_dir variable in the script if your Instagram data files are located elsewhere. The script assumes default filenames for the following and followers HTML files. You can change these in the default_filenames dictionary if needed.

## Error Handling
The script includes basic error handling for file not found and general exceptions during file processing. Error messages will be printed to the console.

## Contributing
Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License
This project is open-source and available under the MIT License.
