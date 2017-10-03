## TK1 ROS code ##

# github upload
1. <pre><code>git add *</code></pre>
2. <pre><code>git commit -m "comments"</code></pre>
3. <pre><code>git push origin master</code></pre>


# Pixhawk <-> Companion Computer Connection
### hardware connection
refer http://www.modulabs.co.kr/board_GDCH80/4986

Using USB to TTL is better i think.

and change PX4 parameter SYS_COMPANION at QGroundControl to CompanionLink(921600 8N1)

### run ROS in TK1
1. run roscore
<pre><code>roscore</code></pre>
2. run Mavros
<pre><code>rosrun mavros mavros_node _fcu_url:="/dev/ttyUSB0:921600"</code></pre>

##### if there is permission problem
<pre><code>sudo chmod 666 /dev/ttyUSB0</code></pre>
##### if you want to see tty list
<pre><code>dmesg | grep tty</code></pre>

#  pixhawk <-> Companion Computer <-> GCS(Linux computer)  Connection
refer http://discuss.px4.io/t/feeding-mavros-using-px4-into-qgc/3499

in companion computer

<pre><code>roscore</code></pre>
<pre><code>roslaunch mavros px4.launch fcu_url:=/dev/ttyUSB0:921600 gcs_url:=udp://@127.0.0.1:14550</code></pre>
here, gcs_url should be a address of GCS(with ros)

# Future work
hardware setting following reference :

https://dev.px4.io/en/ros/offboard_control.html

try arm/disarm, mode change
