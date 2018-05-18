<?php 
use \Workerman\Worker;
use Workerman\Lib\Timer;
use \Workerman\Connection\AsyncTcpConnection;
require_once __DIR__ . '/Workerman/Autoloader.php';

#加载配置文件，后面每10秒更新
$config=parse_ini_file("./config.ini");

#服务器代理
$worker = new Worker('tcp://0.0.0.0:8099');
$worker->count = 1;
$worker->name = '代理机器';


#每个进程启动后在当前进程新增一个Worker监听

$worker->onWorkerStart = function($workers){
	global $config,$worker;

	foreach($config as $key=>$v){
		getClientServer($key);
	}

	Timer::add(10, function()
	{	global $config,$worker;
		$config=parse_ini_file("./config.ini");
		foreach($config as $k=>$v)
		{
			$config[$k]=md5($v);
		}
	});
};


#监听外网连接，做数据中转连接
function getClientServer($port){
	global $worker;
    $inner_worker = new Worker("tcp://0.0.0.0:$port");
    $inner_worker->reusePort = true;
    $inner_worker->port = $port;
    $inner_worker->onMessage =function($connection,$buffer){
		global $worker,$config;
		//数据导向

		if(!isset($worker->connections_clent) or !$worker->connections_clent){
			$connection->send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nad\r\n\r\n客户机不在线，请重试\r\n");
		}else{
			$ip=$config[$connection->worker->port];
			$connections_clent=array_shift($worker->connections_clent[$ip]);
			$msg=$connections_clent->send($buffer);
			
			if(!$msg){
				$connection->send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nad\r\n\r\n内网客户机响应超时\r\n");
				$connection->close();
			}

			$connection->pipe($connections_clent);
			$connections_clent->pipe($connection);
		}
	};

	$inner_worker->listen();
	
	
};
#远程客户端访问代理，中转到中转机上
$worker->onConnect= function($connection){
	global $worker;
	
	if(count($worker->connections)>=500){
		$connection->close();//防止onMessage链接断不开
		return false;
	}

};


$worker->onMessage = function($connection, $buffer)
{
	global $worker,$config;
	#上报MAC
	$buffer=json_decode($buffer,true);
	if(array_key_exists('MAC',$buffer) and array_search(md5($buffer["MAC"]),$config)){
		
		$name=md5($buffer["MAC"]);
		
		if(count(@$worker->connections_clent[$name])<=10){
			$worker->connections_clent[$name][]=$connection;
			echo "中转机连接成功加入连接池 ip " . $connection->getRemoteIp() .":".$connection->getRemotePort()."\n";
		}else{
			$oldconn=array_shift($worker->connections_clent[$name]);
			$oldconn->close();//保持连接池一定水平
			unset($oldconn);
			$worker->connections_clent[$name][]=$connection;;
		}

	}
};

Worker::runAll();