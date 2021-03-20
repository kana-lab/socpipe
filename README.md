# overview
`soctype` provides very simple ways of inter-process communication.  
This only uses `socket`,`json` and `threading` internally, which are standard modules.  
# installation
```pip install socpipe``` or ```pip3 install socpipe```  
# usage
First, please declare some functions like below:  
```
# in process1

def add(a,b):
  return a+b
```
Then, please create `ApiServer` instance and make your APIs visible to other processes.  
```
# in process1

from socpipe import *
api=ApiServer(apis=[add])
api.publish(port=50007)

while True:
  pass
```
where `port` is the port number which will be used by `socket` internally, and you can set whatever number you like.  
After `api.publish` is executed, new thread will be generated and wait connections.  
So you need to prevent process1 from exiting by `while True` or setting `run_forever` variable of `publish` True.  

Let's move on to process2.  
All you have to do is to connect process1 by creating `ApiClient` instance.
```
# in process2

from socpipe import *
api=ApiCient(port=50007)
print(api.add(1,2))
# 3 will be displayed
```
