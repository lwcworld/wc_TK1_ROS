# installed development environment
- ROS
- ROS catkin workspace
- MAVROS
- opencv
- PX4 Firmware (optional. for SITL)
The stable PX4 version is v.1.8.0 : 
<pre><code>git clone --branch DQRC12B https://github.com/PX4/Firmware.git </code></pre>
for multiple quadrotor simulation, 
<pre><code>roslaunch px4 multi_uav_mavros_sitl.launch </code></pre>
if there is error using multiple quadrotors,
- open the single_vehcile_spawn.launch launch file
- Replace this line
<pre><code> arg name="cmd" default="$(find xacro)/xacro.py $(find px4)/Tools/sitl_gazebo/models/rotors_description/urdf/$(arg vehicle)_base.xacro rotors_description_dir:=$(find px4)/Tools/sitl_gazebo/models/rotors_description mavlink_udp_port:=$(arg mavlink_udp_port) > $(arg vehicle)_$(arg ID).urdf ; 'gz sdf -p $(arg vehicle)_$(arg ID).urdf'" /> </code></pre>
by
<pre><code> arg name="cmd" default="$(find xacro)/xacro.py $(find px4)/Tools/sitl_gazebo/models/rotors_description/urdf/$(arg vehicle)_base.xacro rotors_description_dir:=$(find px4)/Tools/sitl_gazebo/models/rotors_description mavlink_udp_port:=$(arg mavlink_udp_port)" /> </code></pre>


# HARDWARE
### Pixhawk <-> Companion Computer Connection
##### hardware connection
refer http://www.modulabs.co.kr/board_GDCH80/4986

Using USB to TTL is better i think.

and change PX4 parameter SYS_COMPANION at QGroundControl to CompanionLink(921600 8N1)

##### run ROS in TK1
1. run roscore
<pre><code>roscore</code></pre>
2. run Mavros
<pre><code>rosrun mavros mavros_node _fcu_url:="/dev/ttyUSB0:921600"</code></pre>

###### if there is permission problem
<pre><code>sudo chmod 666 /dev/ttyUSB0</code></pre>
###### if you want to see tty list
<pre><code>dmesg | grep tty</code></pre>

###  pixhawk <-> Companion Computer <-> GCS(Linux computer)  Connection
refer http://discuss.px4.io/t/feeding-mavros-using-px4-into-qgc/3499

in companion computer

<pre><code>roscore</code></pre>
<pre><code>roslaunch mavros px4.launch fcu_url:=/dev/ttyUSB0:921600 gcs_url:=udp://@127.0.0.1:14550</code></pre>
here, gcs_url should be a address of GCS(with ros)

# SITL
### Option 1
##### term 1
<pre><code>roscore</code></pre>
##### term 2
<pre><code>cd catkin_ws/src/Firmware</code></pre>
<pre><code>source Tools/setup_gazebo.bash $(pwd) $(pwd)/build_posix_sitl_default</code></pre>
<pre><code>no_sim=1 make posix_sitl_default gazebo</code></pre>
##### term 3
<pre><code>source Tools/setup_gazebo.bash $(pwd) $(pwd)/build_posix_sitl_default</code></pre>
<pre><code>roslaunch gazebo_ros empty_world.launch</code></pre>
##### term 4
<pre><code>roslaunch wc_TK1_ROS quad_sitl.launch</code></pre>

### Option 2
##### term 1
<pre><code>roscore</code></pre>
##### term 2
<pre><code>cd catkin_ws/src/Firmware</code></pre>
<pre><code>source Tools/setup_gazebo.bash $(pwd) $(pwd)/build_posix_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
</code></pre>
<pre><code>roslaunch px4 wc_multi_uav_mavros_sitl_1quad.launch</code></pre> or
<pre><code>roslaunch px4 wc_single_uav_withcam_mavros_sitl.launch</code></pre>

# Future work
##### FCU-Companion-GCS hardware connection test
hardware test : https://dev.px4.io/en/ros/offboard_control.html
##### flight test
##### opencv implementation

# github upload
1. <pre><code>git add *</code></pre>
2. <pre><code>git commit -m "comments"</code></pre>
3. <pre><code>git push origin master</code></pre>
