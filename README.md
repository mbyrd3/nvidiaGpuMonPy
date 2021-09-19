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

## Other Copyright Notices  

 Copyright (c) 2011-2020, NVIDIA Corporation.  All rights reserved.  
  
 Redistribution and use in source and binary forms, with or without  
 modification, are permitted provided that the following conditions are met:  
  
    * Redistributions of source code must retain the above copyright notice,  
      this list of conditions and the following disclaimer.  
    * Redistributions in binary form must reproduce the above copyright  
      notice, this list of conditions and the following disclaimer in the  
      documentation and/or other materials provided with the distribution.  
    * Neither the name of the NVIDIA Corporation nor the names of its  
      contributors may be used to endorse or promote products derived from  
      this software without specific prior written permission.  
  
 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  
 ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  
 LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  
 CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  
 SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  
 INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  
 CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  
 ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF  
 THE POSSIBILITY OF SUCH DAMAGE.  

