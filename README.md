# Nvidia Gpu Mon Py (NGMP)
Nvidia Gpu Mon Py is a simple hardware monitoring program which uses pynvml to retrieve the gpu values. It can be used on its own to monitor your hardware locally or, along with NGMP Client, it can be monitored remotely. Compatible with Nvidia GPUs only.

## Features
- Remote monitoring (with Nvidia Gpu Mon Py Client)
- CPU & GPU utilization
- GPU Temperature
- GPU core and memory clock speed & more

## How To Use
Download [Python](https://www.python.org/downloads/) if you don't already have it installed.  
To use, simply run nvidiaGpuMonPy.py  
Values are updated every second.

To set up the server for remote monitoring go to File > Settings, enter your ip address (e.g. 192.168.1.25) and click Done.
After that go to File > Start Server to start the server. For NGMP Client the process is the same, once you enter the server ip address go to File > Connect to Server and you will start receiving.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
