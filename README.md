# Switch Language (Blender Extension)

A lightweight Blender Extension that allows you to instantly toggle between two preferred interface languages using a shortcut key or a UI button. It also gives you precise control over how new data names (like Objects, Materials, and Workspaces) are translated.

## Features

* **Instant Language Toggling:** Switch back and forth between two configured languages (e.g., English and Japanese) without digging through preference menus.
* **Shortcut Key:** Quickly toggle languages using `Ctrl + Alt + L` (fully customizable).
* **Top Bar Button:** A minimalistic globe icon (`🌎`) located in the top-right menu bar for easy mouse access.
* **Name Generation Control:** Choose how Blender names newly created objects. You can sync it with your current language or force it to be "Language Independent" (always English) to avoid multi-byte characters in your project data.
* **Non-intrusive Notifications:** Displays a brief status bar message when the language is switched.

## Requirements

* **Blender 4.2 or newer** (Utilizes the new Blender Extensions system).

##Installation

Since this add-on is built as a Blender Extension, follow these steps to install it from a `.zip` file:

1. **Download the Add-on:** Download the `.zip` release from this repository. *(Note for developers: ZIP the `__init__.py` and `blender_manifest.toml` files directly, not the parent folder).*
2. Open Blender and go to **Edit > Preferences**.
3. Select the **Get Extensions** tab on the left.
4. Click on the downward arrow icon (⌵) in the top right corner and choose **Install from Disk...**.
5. Locate the downloaded `.zip` file and click **Install from Disk**.
6. Ensure the extension is enabled (checked) in the list. 

*Note: Upon activation, Blender will automatically switch to your designated "Language 1" (English by default).*

## ⚙️ Configuration & Usage

Once installed, you can configure the extension by clicking on its settings icon in the **Get Extensions** or **Add-ons** tab.

### Settings Overview

* **Language 1 & Language 2:** Select the two languages you want to switch between. (e.g., English and Japanese).
* **Name Generation:** 
  * `Language 1` / `Language 2`: Newly created data (like a default Cube) will be named based on the selected language's translation.
  * `Language Independent`: New data names will **not** be translated (Always English), regardless of your current UI language. Highly recommended for pipelines that require English naming conventions.
* **Show Notification:** Toggle the status bar info message on/off.
* **Show Topbar Button:** Show or hide the globe icon in the top right of the Blender window.
* **Shortcut Key Setup:** Change the default `Ctrl + Alt + L` shortcut to any key combination you prefer.

## License

This project is licensed under the [GPL-2.0-or-later](https://spdx.org/licenses/GPL-2.0-or-later.html) license, adhering to Blender's official extension guidelines.# Switch Language (Blender Extension)


