# course-selector
A course select helper for Shanghai Koutuu University.

## Parameters:

1st :    &ensp; &emsp; &emsp;   The course type id. It represents the position of tab you want to search under.

2nd:     &ensp; &emsp;&emsp;   What to type in the search box. Course code recommended.

3rd, 4th:   &emsp;   2 keywords contain in the target course. Connected with "and".(Optional)


## Example: 
    python3 main.py 1 EI015 EI015-5

## Environment:
Tested under:

    macos 10.14.6 and Windows 10
    
Requirements:

    pip3 install selenium pytesseract requests
    
Download the corresponding ChromeDriver from: https://chromedriver.chromium.org/ and put it under the "./DRIVER" folder.

<br>
<br>

NOTE: This program may cancel courses that you've selected already to select the new one(s). Use at your own risk.
