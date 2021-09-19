# Nvidia Gpu Mon Py (NGMP)
Nvidia Gpu Mon Py is a simple hardware monitoring program which uses pynvml to retrieve the gpu values. It can be used on its own to monitor your hardware locally or, along with NGMP Client, it can be monitored remotely. Compatible with Nvidia GPUs only.

## Features
- Remote monitoring (with Nvidia Gpu Mon Py Client)
- CPU & GPU utilization
- GPU Temperature
- GPU core and memory clock speed & more

## How To Use  
Download [Python](https://www.python.org/downloads/) if you don't already have it installed.  
Note: You can run the .exe files within both programs folders which can be found in the bin folder. In this case, Python is not needed.  
To use, simply run nvidiaGpuMonPy.py or nvidiaGpuMonPy.exe  
Values are updated every second.

To set up the server for remote monitoring go to File > Settings, enter your ip address (e.g. 192.168.1.25) and click Done.
After that go to File > Start Server to start the server. For NGMP Client the process is the same, once you enter the server ip address go to File > Connect to Server and you will start receiving.  

![image](https://user-images.githubusercontent.com/33243825/133905965-cc333d3f-631a-4ccb-9e5b-61604352f442.png)  
  
![Untitled](https://user-images.githubusercontent.com/33243825/133906074-4cd5d40e-c5ef-48ee-bf91-b398e758fede.png)   
  
![Untitled2](https://user-images.githubusercontent.com/33243825/133906178-f8878428-84e1-4b59-afa5-4a03b9f71e38.png)

## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
