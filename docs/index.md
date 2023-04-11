# Overview

Network config tracker is a tool that monitors the configuration changes of your network devices using a gitlab repository. This tool requires integration to the following applications:

- [Gitlab](https://about.gitlab.com/) which is used for storing the network devices configuration and to monitor the configuration changes.
- [NetBox](https://github.com/netbox-community/netbox) which is used for maintaining the list of network devices to be monitored for configuration changes.


## :material-matrix: Support Matrix
List of supported network device platforms and NetBox parameter configuration.

| Parameters          | Cisco IOS | Cisco IOS-XR | Cisco NXOS    | Juniper JunOS |
| :----------------:  | :-------: | :----------: | :-----------: | :-----------: |
| NetBox Platform     | Cisco IOS | Cisco IOS-XR | Cisco NXOS    | Juniper JunOS |
| NetBox Status       | Active    | Active       | Active        | Active        | 
| NetBox Primary IPv4 | `True`    | `True`       | `True`        | `True`        |
| Login Method        | SSH       | SSH          | SSH \| NX-API | SSH           |

Tested working on:

| Application | Version |
| :---------: | :-----: |
| Python      | 3.9     |
| NetBox      | 3.4.7   |
| GitLab      | 14.1.0  |

## :material-tools: Installation
1. Clone this repository and create a virtual environment.
```
git clone https://github.com/kagarcia1618/Network-Config-Tracker.git
cd network-config-tracker
python3.9 -m venv venv
source venv/bin/activate
```
2. Install the requirements.
```
pip install -r requirements.txt
``` 
3. Create a new directory named private inside the cloned git repository directory.
```
mkdir private
```
4. Prepare the following parameter details:

    * **Username** - to be used to access and get the running configuration of the network devices.
    ```
    admin
    ```
    * **Password** - to be used to access and get the running configuration of the network devices.
    ```
    password
    ```
    * **NetBox URL** - to be used identify the location of local netbox installation.
    ```
    https://<hostname | ipv4 address>
    ```
    * **NetBox API Token** - to be used to access the NetBox URL API and get the list of network devices to be monitored.
    ```
    <api token>
    ```
    * **Gitlab URL** - to be used identify the location of local gitlab installation.
    ```
    https://<hostname | ipv4 address>
    ```
    * **Gitlab Project Name** - to be used to store and monitor the network devices running configuration.
    ```
    kenneth/dev-config/tracker
    ```
    > **Note:** New folder named **`configs`** will be created inside the gitlab project for storing the devices running configuration.
    * **Gitlab Project API Token** - to be used to access the gitlab project via API.
    ```
    <api token>
    ```

5. Generate the encrypted device and application credentials by running `credentials.py` python script. The script will generate your secret key in the private folder together with the encrypted text file for device and application login access. 
```
python credentials.py
```

6. Create a custom field named `Last Config Change` with `date` as type and assign it to `dcim | device`. This will be used by this tool to update the last recorded configuration change for a device.

    **Note:** This tool will also update the device `status` in Netbox based on the result of fetching the device running configuration from the actual device.

## :material-rocket-launch: Usage
1.  Execute the config-tracker.py python script.

    ```
    python config-tracker.py
    ```

    **Note:** If you are using linux environment, you may configure a cronjob to regularly execute this job on your preferred time interval. Sample script below will execute the script every 10 minutes and store output logs to a text file.

    ```
    crontab -e
    */10 * * * * cd ~/network-config-tracker/ && venv/bin/python config-tracker.py  >> logs/access_logs.txt
    ```