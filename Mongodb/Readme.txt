
# MongoDB Installation Guide for Windows (64-bit)

This guide provides step-by-step instructions for downloading and installing MongoDB and MongoDB command-line tools on a Windows (64-bit) system.

## Prerequisites

- Ensure that you have administrative privileges to install software.
- Windows 64-bit operating system.

---

## Step 1: Download MongoDB

1. Go to the official MongoDB website: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Select the following options:
   - **Version**: Choose the latest stable release version.
   - **Platform**: Select **Windows**.
   - **Package**: Choose **MSI**.
3. Click on the **Download** button to download the MongoDB installer.

---

## Step 2: Install MongoDB

1. Run the downloaded `.msi` installer.
2. Follow the on-screen instructions:
   - Accept the license agreement.
   - Choose the **Complete** installation option.
   - Make sure to select the option to **Install MongoDB as a Service**.
   - You can must enable **MongoDB Compass** (the GUI for MongoDB).
3. Once the installation is complete, click **Finish**.

---

## Step 3: Configure Environment Variables

1. Open the **Start Menu** and search for `Environment Variables`.
2. Click on **Edit the system environment variables**.
3. In the **System Properties** window, click on **Environment Variables**.
4. Under the **System variables** section, select `Path` and click **Edit**.
5. Add the MongoDB binaries folder path to the list. The default path is:
   ```
   C:\Program Files\MongoDB\Server\<version>\bin
   ```
   Replace `<version>` with the installed MongoDB version.
6. Click **OK** to close all dialogs.

---

## Step 4: Verify MongoDB Installation

1. Open **Command Prompt** (press `Win + R`, type `cmd`, and press Enter).
2. Type the following command to check if MongoDB is installed correctly:
   ```
   mongod --version
   ```
   If MongoDB is successfully installed, this command will display the MongoDB version.

---

## Step 5: Download and Install MongoDB Command Line Tools

1. Go to the following MongoDB Tools download page: [https://www.mongodb.com/try/download/database-tools](https://www.mongodb.com/try/download/database-tools)
2. Choose **Windows** as the platform and download the `.zip` package.
3. Extract the `.zip` file to a directory of your choice.
4. Add the path to the extracted folder (containing the command-line tools) to your system `Path` environment variable, similar to Step 3.

---

## Step 6: Verify MongoDB Command-Line Tools

1. Open **Command Prompt**.
2. Type any MongoDB tool command to verify the installation. For example:
   ```
   mongoexport --version
   ```
   This command should display the version of `mongoexport`.

---

## Step 7: Starting MongoDB

1. In **Command Prompt**, type the following to start MongoDB:
   ```
   mongod
   ```
2. Open a new **Command Prompt** window, and type the following command to connect to the MongoDB server:
   ```
   mongo
   ```

Congratulations! MongoDB and its command-line tools are now installed on your Windows 64-bit system.

---

## Additional Information

- [MongoDB Documentation](https://www.mongodb.com/docs/)
```

This `README.md` file provides detailed instructions for installing MongoDB and its tools on a Windows 64-bit system.