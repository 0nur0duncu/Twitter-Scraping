# Twitter Monitor

Twitter Monitor is a Python application that automatically tracks specified Twitter/X accounts, detects new tweets, and saves media content.

## 🚀 Features

- Simultaneous monitoring of multiple Twitter accounts
- Automatic detection and logging of new tweets
- Automatic download of media content (images) from tweets
- Detailed logging system
- Random User-Agent usage for realistic user simulation
- State management for tracking latest tweets

## 📋 Requirements

```
- Python 3.7+
- selenium
- fake-useragent
- Chrome WebDriver
```

## 🛠️ Installation

1. Install required Python packages:
```bash
pip install selenium fake-useragent
```

2. Install Chrome WebDriver:
   - For Windows: [Chrome WebDriver Download Page](https://sites.google.com/chromium.org/driver/)
   - For Linux: `sudo apt-get install chromium-chromedriver`

3. Clone or download the project
```bash
git clone [repo-url]
cd twitter-monitor
```

## 💻 Usage

1. Edit the `accounts` list:
```python
accounts = [
    'cnbceofficial',
    'FintablesHaber',
    'fintables',
    'binance'
]
```

2. Start the application:
```bash
python twitter_monitor.py
```

## 📁 File Structure

```
twitter-monitor/
│
├── twitter_monitor.py      # Main application file
├── last_tweets.json       # File storing latest tweets
├── tweets_log.txt         # Tweet records file
├── twitter_monitor.log    # Application logs
└── images/               # Directory for downloaded images
```

## ⚙️ Configuration

### Scanning Interval
The default scanning interval is 300 seconds (5 minutes). You can change this by specifying a different `interval` value when calling the `monitor()` method:

```python
monitor.monitor(interval=600)  # Check every 10 minutes
```

### Chrome Settings
Chrome driver settings can be configured in the `setup_driver()` method. Default settings include:
- Headless mode (background operation)
- Disabled notifications
- Disabled extensions
- Disabled GPU usage

## 📊 Logging

The application maintains two different log files:

1. `twitter_monitor.log`: Application status and error logs
2. `tweets_log.txt`: Detailed records of detected new tweets

## 🛡️ Security Measures

- Random User-Agent implementation
- Random delays between requests
- Headless mode operation
- Basic Chrome security settings

## ⚠️ Error Handling

The application handles the following scenarios:
- Network connection errors
- Page loading timeouts
- Element not found situations
- Image download errors

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📫 Contact

Project Maintainer: [Name]
Project Link: [GitHub Repo URL]

## 🙏 Acknowledgments

- Selenium team
- fake-useragent developers
- All contributors

## 🔍 Technical Details

### Main Components

#### TwitterMonitor Class
The main class that handles all monitoring operations:
- Initializes WebDriver with custom options
- Manages state through JSON file
- Handles image downloads and logging
- Implements retry mechanisms and error handling

#### Key Methods
- `setup_driver()`: Configures Chrome WebDriver with appropriate options
- `check_account()`: Monitors individual accounts for new tweets
- `extract_tweet_info()`: Parses tweet data from webpage elements
- `download_image()`: Handles media content download and storage
- `monitor()`: Main loop that orchestrates the monitoring process

### State Management
The application maintains state through `last_tweets.json`, which stores:
- Account names
- IDs of latest processed tweets
- Timestamps of last checks

### Error Recovery
- Automatic retry on network failures
- Graceful handling of rate limiting
- Session recovery after crashes

## 🔧 Advanced Configuration

### Custom User Agents
You can modify the User-Agent rotation by editing the `setup_driver()` method:
```python
options.add_argument(f'user-agent={your_custom_user_agent}')
```

### Proxy Support
To add proxy support, modify the Chrome options:
```python
options.add_argument('--proxy-server=your_proxy_address')
```

### Custom Download Paths
Modify the image download path in the initialization:
```python
self.images_folder = 'your/custom/path'
```