from onem2m import *
# Declaring variables
uri_cse = "http://127.0.0.1:8080/~/in-cse/in-name"
ae = "Readings"
cnt1 = "Current_rpm"
cnt2 = "Average_rpm"
cnt3 = "Session_time"
cnt4 = "Distance"
cnt5 = "Start_flag"
cnt6 = "Session_id"

uri_ae = uri_cse+"/"+ae
uri_cnt1 = uri_ae + "/" + cnt1
uri_cnt2 = uri_ae + "/" + cnt2
uri_cnt3 = uri_ae + "/" + cnt3
uri_cnt4 = uri_ae + "/" + cnt4
uri_cnt5 = uri_ae + "/" + cnt5
uri_cnt6 = uri_ae + "/" + cnt6
#
delete_ae(uri_ae)
# Functions
create_ae(uri_cse, ae)
create_cnt(uri_ae,cnt1)
create_cnt(uri_ae,cnt2)
create_cnt(uri_ae,cnt3)
create_cnt(uri_ae,cnt4)
create_cnt(uri_ae,cnt5)
create_cnt(uri_ae,cnt6)

'''
create_data_cin(uri_cnt5,"1")
create_data_cin(uri_cnt1,"5")
create_data_cin(uri_cnt1,"7")
create_data_cin(uri_cnt1,"8")
create_data_cin(uri_cnt1,"35")
create_data_cin(uri_cnt5,"0")

create_data_cin(uri_cnt2,"-1")
create_data_cin(uri_cnt3,"-1")
create_data_cin(uri_cnt4,"-1")
create_data_cin(uri_cnt5,"0")
create_data_cin(uri_cnt5,"-1")
'''