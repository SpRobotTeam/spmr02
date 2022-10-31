#! /usr/bin/env python3

from cgi import test
import canopen
import time

# Start with creating a network representing one CAN bus
network = canopen.Network()

# Connect to the CAN bus
# network.connect(bustype='kvaser', channel=0, bitrate=1000000)
# network.connect(channel='can1', bustype='socketcan')
network.connect(bustype ='slcan', channel ='/dev/ttyACM0', bitrate = 1000000)


network.check()

eds_path = "/home/tang/catkin_ws/src/spmr02/nodes/Smartris_eds_fw_226.eds"

# Add some nodes with corresponding Object Dictionaries
node_01 = canopen.BaseNode402(0x01, eds_path)
network.add_node(node_01)

node_02 = canopen.BaseNode402(0x02, eds_path)
network.add_node(node_02)

# # Reset network
# node_01.nmt.state = 'RESET COMMUNICATION'
# node_02.nmt.state = 'RESET COMMUNICATION'

# node_01.nmt.state = 'RESET'
# time.sleep(1)
# node_02.nmt.state = 'RESET'
# time.sleep(1)

# node_01.nmt.wait_for_bootup(15)
# node_02.nmt.wait_for_bootup(15)


# def Reset_All():
#     node_01.nmt.state = 'RESET COMMUNICATION'
#     node_02.nmt.state = 'RESET COMMUNICATION'
#     node_01.nmt.state = 'RESET'
#     node_02.nmt.state = 'RESET'
#     node_01.nmt.wait_for_bootup(15)
#     node_02.nmt.wait_for_bootup(15)

def Reset_All():
    node_01.nmt.state = 'RESET COMMUNICATION'
    node_02.nmt.state = 'RESET COMMUNICATION'
    node_01.nmt.state = 'RESET'
    node_02.nmt.state = 'RESET'
    node_01.nmt.wait_for_bootup(15)
    node_02.nmt.wait_for_bootup(15)
    print("Reset 진행 중...")
    time.sleep(7)  
    if (node_01.sdo[0x6041].raw == 592 and node_02.sdo[0x6041].raw == 592):
        time.sleep(1)
        print("Reset_All 완료") 

# def Para_Set():
#     node_01.sdo[0x6060].raw = 0x03 # “Profile velocity”
#     time.sleep(1)        
#     node_02.sdo[0x6060].raw = 0x03  # “Profile velocity”
#     time.sleep(1)
#     node_01.sdo[0x6040].raw = 0x06  # “Ready to Switch On” 
#     time.sleep(1)       
#     node_02.sdo[0x6040].raw = 0x06  # “Ready to Switch On”
#     time.sleep(1)
#     node_01.sdo[0x6040].raw = 0x07  # “Switched On"    
#     time.sleep(1)    
#     node_02.sdo[0x6040].raw = 0x07  # “Switched On" 
 
def Para_Set():              
    if (node_01.sdo[0x6041].raw == 592 and node_02.sdo[0x6041].raw == 592):
        time.sleep(1)
        node_01.sdo[0x6060].raw = 0x03 # “Profile velocity”
        time.sleep(1)        
        node_02.sdo[0x6060].raw = 0x03  # “Profile velocity”
        time.sleep(1)
    
        if (node_01.sdo[0x6061].raw == 3 and node_02.sdo[0x6061].raw==3):
            print("profile velocity 설정완료")
            node_01.sdo[0x6040].raw = 0x06  # "RW Shutdown"
            time.sleep(1)
            node_02.sdo[0x6040].raw = 0x06  # “ LW Shutdown” 
            time.sleep(1)                               

            if (node_01.sdo[0x6041].raw == 4657 and node_02.sdo[0x6041].raw == 4657):
                print("Shutdown 설정완료")
                node_01.sdo[0x6040].raw = 0x07 # “RW Switched On" 
                time.sleep(1)
                node_02.sdo[0x6040].raw = 0x07 # “LW Switched On"
                time.sleep(1)

                if (node_01.sdo[0x6040].raw == 0x07 and node_02.sdo[0x6040].raw == 0x07):
                    print("Para_set 설정이 완료되었습니다.")    

                else:
                    print("4단계 실패...Para_set 설정에 실패하였습니다. Para_Set()을 다시 실행시켜주세요.")
    
            else:               
                print("3단계 실패...Shutdown 이 제대로 작동되지 않았습니다. Para_Set()을 다시 실행시켜주세요.")

        else: 
            print("2단계 실패...Modes of Operation 값이 입력되지 않았습니다. Para_Set()을 다시 실행시켜주세요.")
    
    else:
        print("1단계 실패...Reset_All()후 Para_Set()을 실행해주십시오.")

# def Dir_Op():
#     Para_Set()
#     time.sleep(1)
#     node_01.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
#     time.sleep(1)        
#     node_02.sdo[0x6040].raw = 0x0f  # “Operation Enabled”

def Dir_Op():

    if (node_01.sdo[0x6040].raw == 0x07 and node_02.sdo[0x6040].raw == 0x07):
        time.sleep(1)
        node_01.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
        print("RW Dir_Op완료") 
        time.sleep(1)        
        node_02.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
        print("LW Dir_Op완료")
    
    else:
        Para_Set()
        time.sleep(1)
        node_01.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
        print("RW Dir_Op완료")
        time.sleep(1)        
        node_02.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
        print("LW Dir_Op완료")


def RW_Move(right):
    Pre_RW_Vel = right
    # RW_Vel = int(Pre_RW_Vel) * 22
    RW_Vel = Pre_RW_Vel * 22
    node_01.sdo[0x60ff].raw = RW_Vel

def LW_Move(left):
    Pre_LW_Vel = left
    # LW_Vel = int(Pre_LW_Vel) * 22
    LW_Vel = Pre_LW_Vel * 22
    node_02.sdo[0x60ff].raw = LW_Vel

def Syn_Move():
    Pre_Syn_Vel = input()
    Syn_Vel = int(Pre_Syn_Vel) * 22
    node_01.sdo[0x60ff].raw = Syn_Vel
    node_02.sdo[0x60ff].raw = Syn_Vel

def Monitor_Val():
    Vel_Dem = [node_01.sdo[0x606B].raw, abs(node_02.sdo[0x606B].raw)]
    print("Velocity Demand Value :", Vel_Dem)
    Vel_Act_vel = [node_01.sdo[0x606C].raw, abs(node_02.sdo[0x606C].raw)]
    print("Velocity Actual Value :", Vel_Act_vel)        
    Pos_Act = [node_01.sdo[0x6064].raw, abs(node_02.sdo[0x6064].raw)]
    print("Position Actual Value :", Pos_Act)

def Syn_STOP():        
    node_01.sdo[0x60ff].raw = 0
    node_02.sdo[0x60ff].raw = 0

def RW_STOP():        
    node_01.sdo[0x60ff].raw = 0

def LW_STOP():
    node_02.sdo[0x60ff].raw = 0

##############################
##########Torque def##########
def Tor_Op():
    node_01.sdo[0x6060].raw = 0x04 # “Profile Torque”
    time.sleep(1)        
    node_02.sdo[0x6060].raw = 0x04  # “Profile Torque”
    time.sleep(1)
    node_01.sdo[0x6040].raw = 0x06  # “Ready to Switch On” 
    time.sleep(1)       
    node_02.sdo[0x6040].raw = 0x06  # “Ready to Switch On”
    time.sleep(1)
    node_01.sdo[0x6040].raw = 0x07  # “Switched On"    
    time.sleep(1)    
    node_02.sdo[0x6040].raw = 0x07  # “Switched On" 
    time.sleep(1)
    node_01.sdo[0x6040].raw = 0x0f  # “Operation Enabled”
    time.sleep(1)        
    node_02.sdo[0x6040].raw = 0x0f  # “Operation Enabled”

def Tor_Move(set):        
    Tor_Vel = set        
    node_01.sdo[0x6071].raw = Tor_Vel
    node_02.sdo[0x6071].raw = Tor_Vel
        
def Tor_Moni():
    Tor_Act_val = [node_01.sdo[0x6077].raw, abs(node_02.sdo[0x6077].raw)]
    print("Torque Actual Value :", Tor_Act_val)
    Vel_Act_vel = [node_01.sdo[0x606C].raw, abs(node_02.sdo[0x606C].raw)]
    print("Velocity Actual Value :", Vel_Act_vel)        
    Pos_Act = [node_01.sdo[0x6064].raw, abs(node_02.sdo[0x6064].raw)]
    print("Position Actual Value :", Pos_Act)        

def off():
    node_01.nmt.state = 'RESET'
    node_02.nmt.state = 'RESET'
    network.sync.stop()
    network.disconnect()

    
# Reset_All()
# time.sleep(5)

# Dir_Op()

# RW_Move(60)
# LW_Move(60)

# Syn_STOP()
# time.sleep(0.5)
# off()

