
import socket
import json
import threading

# USAGE:
#   
#   # server.py
#   def add(a,b): return a+b
#   api=ApiServer(apis=[add])
#   api.publish(50007,run_forever=False)
#   while True: time.sleep(1)
#   
#   # client.py
#   api=ApiClient(50007)
#   print(api.add(3,4))
#   

class _SocManager:
	def __init__(self,port,host):
		self.s=None
		for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, 
										socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa=res
			try:
				self.s=socket.socket(af, socktype, proto)
			except OSError as msg:
				self.s=None
				continue
			try:
				self.s.bind(sa)
				self.s.listen(1)
			except OSError as msg:
				self.s.close()
				self.s=None
				continue
			break
		if self.s is None:
			raise Exception('could not open socket')
	
	def wait_client(self,callback):
		with self.s:
			while True:
				conn, addr=self.s.accept()
				callback(_Client(conn))


class _Client:
	def __init__(self,conn):
		self.conn=conn
		self.callback=lambda d: {'success':False,'return':None,'msg':'server error: no bind'}
	
	def set_callback(self,callback):
		self.callback=callback
	
	def start(self):
		threading.Thread(target=self._recv,daemon=True).start()
	
	def _recv(self):
		with self.conn:
			with self.conn.makefile('r',encoding='utf-8') as conn_in:
				while True:
					data=conn_in.readline().rstrip()
					if not data:
						return
					data=json.loads(data) # { 'function':'hogehoge','args':[],'kwargs':{} }
					self.send(self.callback(data))
	
	def send(self,obj):
		self.conn.sendall((json.dumps(obj)+'\n').encode())


class ApiServer:
	def __init__(self,apis):
		self.api_list=apis
	
	def _requested(self,dc):
		ret={'success':True,'return':None,'msg':''}
		for func in self.api_list:
			if dc['function']==func.__name__:
				try:
					ret['return']=func(*dc['args'],**dc['kwargs'])
				except Exception as e:
					ret['success']=False
					ret['msg']=repr(e)
				return ret
		else:
			ret['success']=False
			ret['msg']=f'No function named {dc["function"]}'
			return ret
	
	def publish(self,port,host='localhost',run_forever=False):
		s=_SocManager(port,host)
		
		def callback(client):
			client.set_callback(self._requested)
			client.send([func.__name__ for func in self.api_list])
			client.start()
		
		if run_forever:
			s.wait_client(callback)
		else:
			threading.Thread(target=s.wait_client,args=(callback,),daemon=True).start()


class _ApiCallable:
	def __init__(self,name,callback):
		self.name=name
		self.callback=callback
	
	def __call__(self,*args,**kwargs):
		dc={'function':self.name,'args':args,'kwargs':kwargs}
		return self.callback(dc)


class ApiClient:
	def __init__(self,port,host='localhost'):
		self.s, self.file=None, None
		for res in socket.getaddrinfo(host,port):
			af, socktype, proto, canonname, sa=res
			try:
				self.s=socket.socket(af, socktype, proto)
			except:
				continue
			try:
				self.s.connect(sa)
			except:
				self.s.close()
				continue
			break
		else:
			self.s=None
			raise Exception('could not open socket.')
		self.file=self.s.makefile('r',encoding='utf-8')
		
		self.apis=json.loads(self.file.readline().rstrip())
		for func in self.apis:
			setattr(self,func,_ApiCallable(func,self.request))
	
	def request(self,dc):
		self.s.sendall((json.dumps(dc)+'\n').encode())
		ret=json.loads(self.file.readline().rstrip())
		if not ret['success']:
			raise Exception(ret['msg'])
		else:
			return ret['return']
	
	def __del__(self):
		if self.file is not None: self.file.close()
		if self.s is not None: self.s.close()


