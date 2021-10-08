# Network Config Tracker

Network config tracker is a tool that monitors the configuration changes of your network devices using a local gitlab repository. This tool requires integration to the following applications:

- [Gitlab](https://about.gitlab.com/) which is used for storing the network devices configuration and to monitor the configuration changes.
- [NetBox](https://github.com/netbox-community/netbox) which is used for maintaining the list of network devices to be monitored for configuration changes.

### How to Use

1. Clone this git repository to your local linux environment.
2. Create a local python virtual environment inside the cloned git repository directory.
    ```
    cd ~/network-config-tracker
    python3.6 -m venv venv
    source venv/bin/activate
    ```
3. Pip install the required modules.
    ```
    pip install -r requirements.txt
    ```
4. Create a new directory named `private` inside the cloned git repository directory.
    ```
    mkdir private
    ```
5. Generate the necessary device and application credentials by running `credentials.py` python script. The script will generate your secret key in the private folder together with the encrypted text file for device and application credentials. Prepare the following details before running the script:

    - **Network Device Username and Password** to be used to access and get the running configuration of the network devices.

    - **NetBox URL** to be used identify the location of local netbox installation.

    - **NetBox API Token** to be used to access the NetBox URL API and get the list of network devices to be monitored

    - **Gitlab Project Name** to be used to store and monitor the network devices running configuration.

    - **Gitlab URL** to be used identify the location of local gitlab installation.

    - **Gitlab Project API Token** to be used to access the gitlab project via API.

    ```
    python credentials.py
    ```

6. Make sure that your Netbox has at least network devices registered on it with the following criteria:
    
    - Devices should have `Primary IPv4` assigned.

    - Devices should at least be under the following platform names: `Cisco NXOS`, `Cisco IOS`, `Cisco IOS-XR` and `Juniper JunOS`
7. Make sure that your local environment running this tool is able to access your Netbox URL, Gitlab URL and network devices.
8. Create a custom field named `Last Config Change` with `date` as type and assign it to `dcim | device`. This will be used by this tool to update the last recorded configuration change for a device.

    **Note:** This tool will also update the device `status` in Netbox based on the result of fetching the device running configuration from the actual device. 
9. Execute the `config-tracker.py` python script.

    ```
    python config-tracker.py
    ```

    **Note:** If you are using linux environment, you may configure a cronjob to regularly execute this job on your preferred time interval. Sample script below will execute the script every 10 minutes and store output logs to a text file.

    ```
    crontab -e
    */10 * * * * cd ~/network-config-tracker/ && venv/bin/python config-tracker.py  >> logs/access_logs.txt
    ```
10. Verify that the devices running configuration is created in your local gitlab project repository.
