# osc-watch

**osc-watch** is a simple web-based tool for monitoring a directory for new or moved files and sending notifications via OSC (Open Sound Control) messages. It provides a web interface to configure the directory to watch and the OSC target, and displays a real-time log of events.

## Features

- Monitor a directory for new or moved files.
- Send OSC messages (`/newfile`) with filename and timestamp to a specified IP and port.
- Web interface for configuration and control.
- Real-time log of events via the browser.
- Send test OSC messages to verify connectivity.

## Requirements

- Python 3.7+
- [Flask](https://flask.palletsprojects.com/)
- [python-osc](https://pypi.org/project/python-osc/)
- [watchdog](https://pypi.org/project/watchdog/)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/osc-watch.git
   cd osc-watch
   ```
2. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```sh
   python app.py
   ```
4. **Access the web interface:**
   Open your web browser and go to `http://localhost:5000`.

## Usage

1. **Configure the directory to watch:**
   Enter the path of the directory you want to monitor in the web interface.

2. **Set the OSC target:**
   Specify the IP address and port number where OSC messages should be sent.

3. **Start monitoring:**
   Click the "Start" button in the web interface to begin monitoring the directory.

4. **View events:**
   Real-time events will be displayed in the web interface log.

5. **Test OSC connectivity:**
   Use the "Send Test OSC" button to send a test message to the specified OSC target.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for a flexible and easy-to-use file monitoring solution.
- Thanks to the contributors and open-source libraries that made this project possible.