<p align="center">
  <img alt="GSR" src="https://github.com/MrSaighnal/GSR-Google-Slides-RAT/blob/main/images/GSR_logo.png?raw=true" height="200" /><br />
<a href="https://twitter.com/mrsaighnal"><img src="https://img.shields.io/twitter/follow/mrsaighnal?style=social" alt="twitter" style="text-align:center;display:block;"></a>

</p>
<p align="left">

# GSR - Google Slides RAT
Google Slides RAT (GSR) is the evolution of the previously established [Google Calendar RAT](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT).
GSR serves as a proof of concept for an infrastructure-less Command&Control (C2) mechanism utilizing Google Slides documents. This tool is beneficial for scenarios where exposing a Red Teaming infrastructure is undesirable, and there's a need to streamline deployment. To employ GSR, one only needs a Gmail account. The script establishes a 'Covert Channel' by exploiting the table content within a Google Slides document, allowing the target to connect directly to Google. It could potentially be classified as a Layer 7 application covert channel.

![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/25ad5023-1b8d-4d39-9e8e-f632351f2708)

## POC
![animation](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/293df586-38f9-4803-a201-e716f518954e)

## How to use
1. The C2 can be directly cloned from GitHub by using the following commands:

    ```
    git clone https://github.com/MrSaighnal/GSR-Google-Slides-RAT
    cd GSR-Google-Slides-RAT
    ```
2. **Enable the Google Slides API**
   Visit https://console.cloud.google.com/apis/library/slides.googleapis.com?project=<p>
   ![api](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/f7dfbcfb-41f8-4b57-a1a5-fb69626ace16)

3. **Create a new service account and download the JSON file containing the credentials**
   Create a new service account and download the JSON file containing the credentials by navigating to https://console.cloud.google.com/, exploring the "IAM & Admin" section, and then clicking on "Service Accounts" in the left panel.
   ![saccount](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/67746089-8790-4cae-8eef-5cb0dae18764)<p>
   Proceed with the account creation. In the account panel, click on "Add Key", then choose "Create new key", and select the JSON format.
   ![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/2df962e1-925e-4b5a-84ab-3b60f7b0f270)<p>
   
4. **Create a new Google Slides document and note of its ID (in the URL)**
   ![slide](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/81c27b11-4de0-488c-b4d9-0fce3902deb8)
   
5. **Share the Google document with the newly created service account**
   ![share](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/f9456977-ec50-484c-8fc0-4e78d40a71c7)
   
6. **Configure the C2**
   Paste the contents of the credentials JSON file and the document ID (retrieved from the URL) into `server/modules/config.py` and `agent/agent.py`.

7. **Configure the Google Slides document**
   Create a table in the first slide consisting of 3 columns and multiple rows (5 or more is highly suggested).
    ![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/2e39b080-632f-4317-b992-c5fce27a456b)
    
8. **Weaponize your agent.py file, and deliver it to the target**
    To weaponize your agent.py file and deliver it to the target, you can use various methods. For a straightforward approach, use PyInstaller with the following command:<p>
    ```
    pyinstaller --noconfirm --onefile --windowed  "C:/Users/Admin/Documents/Progetti/GSC - Google Slides Rat/agent/agent.py"
    ```

    Alternatively, you can use auto-py-to-exe as follows:<p>
    ![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/358d8c25-da99-405d-a8d9-380f9e04d565)

9. **Enjoy your C2**
   Open the shell by running the file `main.py` within `server/`
   by running
   ```
   cd server;
   python main.py
    ```

## Attack Workflow
![GSR - Google Slides RAT](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/38d191ab-27d4-44d3-96cc-09f073bc63bf)

## How it works
GSR consists of two main components:
- the agent
- the server

The agent is the component that needs to be deployed on the target PC. It's entirely written in Python and can be weaponized with the help of auto-py-to-exe.

The server allows for comfortable Command&Control, interfacing directly with Google's services.

## What a SOC Analyst will see?
Concentrating solely on the networking component, the only links formed will be with Google's servers, rendering the connection entirely authentic. We'll verify this using Process Explorer.<p>
![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/4a2c8a2c-5d26-4f4b-ad7c-5ffe31180d63)

which results in
![image](https://github.com/MrSaighnal/GSR-Google-Slides-RAT/assets/47419260/ffed687c-b9f9-433b-a5f9-921be16ce70e)

## Disclaimer and notes
Google Slides RAT has been made in Italy with ❤️<p>
I take no responsibility for the use that will be made of it.<p>
Please do not use it for illegal purpose.

## To do
- [x] Agent Development
- [x] C2 (Command and Control) Development
- [x] Command Execution (via bi-directional communication channel)
- [ ] Change Polling Time Function
- [ ] Screenshot Capture Function
- [ ] File Download
- [ ] File Upload
- [ ] Cryptographic Protocol
