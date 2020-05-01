<!-- PROJECT LOGO -->

<!-- <p align="center">
  <img src="img\logo.png" alt="Logo" width="80" height="80">
</p> -->

## EmailTrigger_OnFileChange

[![HitCount](http://hits.dwyl.com/VRB95/VRB95/EmailTrigger_OnFileChange.svg)](http://hits.dwyl.com/VRB95/VRB95/EmailTrigger_OnFileChange) [![License: MIT](https://img.shields.io/github/license/VRB95/EmailTrigger_OnFileChange?color=blue&style=flat-square)](https://opensource.org/licenses/MIT)

This project describe the usage of [QFileSystemWatcher Class](https://doc.qt.io/archives/qt-4.8/qfilesystemwatcher.html) which monitors the file system for changes to files and directories by watching a list of specified paths. When the file that is monitored is changed in some way, a signal is emited and with the help of [smtplib — SMTP protocol client](https://docs.python.org/3/library/smtplib.html) an email is send tot an specific address. For simplicity, an User Interface was created with PyQt4.

<p align="center">
  <img src="img\screensh_1.png" alt="screenshot_1">
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Built With:
* [Python](https://www.python.org)
* [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download) 
* [smtplib](https://docs.python.org/3/library/smtplib.html)

## Prerequisites

I'll asume you already have installed python 3.x, now install [PyQt4](ttps://www.riverbankcomputing.com/software/pyqt/download). PyQt4 is now deprecated, but you can download the right .whl file for your OS from [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) and use:

```sh
 pip install filename.whl
```


<!-- USAGE EXAMPLES -->
## Usage

All the data, like password, sender email, reciver email and so on are stored in a configuration file (*.ini). When the program is started all the data from the config. file are loaded, those data can be alterated to form a new config. file. This is the first step, open the config file whith any txt editor and complet all fields (the path for the file can be completed from UI, so leave it blank for now).
After this, sust run:

```sh
python main.py
 ```

in the repo folder. The UI will apear on screen. Now select the file you want to be monitored and now just... wait?
The UI and also the config file have a field for delay. This delay is a "countdown" which start after any modification are made on the watched file, only after all the seconds from the delay spinbox are passed the email is send to a specified address.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Vesa Bogdan - vesabogdan95@gmail.com

Project Link: [https://github.com/vesa95/SimpleSync](https://github.com/vesa95/SimpleSync)





<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square
[contributors-shield]: https://img.shields.io/badge/contributors-1-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-url]: https://choosealicense.com/licenses/mit
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/screenshot.png
