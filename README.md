# overview
`socpipe` provides very simple ways of inter-process communication.  
This only uses `socket`,`json`, and `threading` internally, which are standard modules.  
# installation
`pip install socpipe` or `pip3 install socpipe`  
# usage
First, please define some functions like below:  
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
where `port` is the port number that will be used by `socket` internally, and you can set whatever number you like.  
After `api.publish` is executed, a new thread will be generated and wait for connections.  
So you need to prevent process1 from exiting by `while True` or setting `run_forever` parameter of `publish` True.  

Let's move on to process2.  
All you have to do is to connect process1 by creating `ApiClient` instance.
```
# in process2

from socpipe import *
api=ApiCient(port=50007)
print(api.add(1,2))
# 3 will be displayed
```
By the way, `publish` and `ApiClient` also has a parameter `host`, so you can communicate with remote hosts by setting this parameter.  
I haven't tested this function, though.
# 概要
`socpipe`はプロセス間通信のための大変シンプルな関数を提供します。  
このモジュールは内部で標準モジュールである`socket`,`json`,`threading`のみを使用しています。  
# インストール
`pip install socpipe` または `pip3 install socpipe`  
# 使い方
まず、次のように適当な関数を定義して下さい。  
```
# in process1

def add(a,b):
  return a+b
```
そして、`ApiServer`インスタンスを作り、あなたのAPIを他のプロセスに公開します。  
```
# in process1

from socpipe import *
api=ApiServer(apis=[add])
api.publish(port=50007)

while True:
  pass
```
ここで、`port`は内部で`socket`によって使われるポート番号であり、好きな番号をセットして構いません。  
`api.publish`が実行されると、新しいスレッドが生成され他のプロセスからの接続を待つようになります。  
よって、process1が終了してしまわないように、`while True`を付け足すか、または`publish`の`run_forever`引数をTrueにセットする必要があります。  

process2に移りましょう。
`ApiClient`インスタンスを作ってprocess1に接続するだけです。  
```
# in process2

from socpipe import *
api=ApiCient(port=50007)
print(api.add(1,2))
# 3 will be displayed
```
ところで、`publish`と`ApiClient`は`host`という引数も持っており、これをセットすることでリモートホストと通信することが出来ます。  
ただ、この機能は未テストです。  
