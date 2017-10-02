## TK1 ROS code ##

# github upload
1. <pre><code>git add *</code></pre>
2. <pre><code>git commit -m "comments"</code></pre>
3. <pre><code>git push origin master</code></pre>


# Connection to Pixhawk
### hardware connection
refer http://www.modulabs.co.kr/board_GDCH80/4986

Using USB to TTL is better i think.

### run ROS in TK1
1. run roscore
<pre><code>roscore</code></pre>
2. run Mavros
<pre><code>rosrun mavros mavros_node _fcu_url:="/dev/ttyUSB0:921600"</code></pre>

##### if there is permission problem
<pre><code>sudo chmod 666 /dev/ttyUSB0</code></pre>
##### if you want to see tty list
<pre><code>dmesg | grep tty</code></pre>
