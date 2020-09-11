import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


def delete_first_line(path5):
    dataframe = pd.read_csv(path5, sep=",", header=0)

    df = dataframe.to_csv(path5.replace('.csv', '_no_header.csv'), index=None, header=None)

    return path5.replace('.csv', '_no_header.csv')

def reindex(path3):
    whole_dataframe = pd.read_csv(path3, sep=",")

    whole_dataframe = whole_dataframe.sample(frac=1)

    df = whole_dataframe.to_csv(path3.replace('.csv', '_reindexed.csv'), index=None,header=None)

    return path3.replace('.csv', '_reindexed.csv')


class data_handling:

    def __init__(self, path1=None,path2=None,path3=None):
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3





    ########   handling KDD99 raw datas
    def handle_kdd99(self):
        kdd99_dataframe = pd.read_csv(self.path1,sep=",")

        #adding title for process
        kdd99_dataframe.columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins", "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_hot_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]

        #remove kdd redundant column
        kdd99_dataframe = kdd99_dataframe.drop(["hot","num_failed_logins", "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_hot_login","is_guest_login"],axis=1)

        # change label format
        for i in range(len(kdd99_dataframe)):
            if kdd99_dataframe["label"][i] in ["back.","land.","neptune.","pod.","smurf.","teardrop."]:
                kdd99_dataframe["label"][i] = "dos"
            elif kdd99_dataframe["label"][i] in ["ipsweep.","nmap.","portsweep.","satan."]:
                kdd99_dataframe["label"][i] = "scan"
            elif kdd99_dataframe["label"][i] in ["ftp_write.","guess_passwd.","imap.","multihop.","phf.","spy.","warezclient.","warezmaster."]:
                kdd99_dataframe["label"][i] = "r2l"
            elif kdd99_dataframe["label"][i] in ["buffer_overflow.","loadmodule.","perl.","rootkit."]:
                kdd99_dataframe["label"][i] = "u2r"
            else:
                kdd99_dataframe["label"][i] = "normal"

        df = kdd99_dataframe.to_csv(self.path1.replace('.csv', '_kdd99_handled.csv') ,index = None)
        return self.path1.replace('.csv', '_kdd99_handled.csv')


    ###### handling kdd99-extracted packet information
    def handle_new(self):
        

        new_dataframe = pd.read_csv(self.path2,sep=",")

        # adding title
        new_dataframe.columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","lhost","lport","rhost","rport","time_stamp","label"]

        # adding useful protocol information transform 445 and 3389 port to protocol name
        for i in range(len(new_dataframe)):
            if new_dataframe["rport"][i] == 445:
                new_dataframe["service"][i] = "smb"
            elif new_dataframe["rport"][i] == 3389:
                new_dataframe["service"][i] = "rdp"

        # drop useless column

        new_dataframe = new_dataframe.drop(["lhost","lport","rhost","rport","time_stamp"],axis=1)
        
    
        df = new_dataframe.to_csv(self.path2.replace('.csv', '_new_handled.csv') ,index = None)

        return self.path2.replace('.csv', '_new_handled.csv')


    # SOME title-needed MERGING FUNCTIONS,should preserve the title of csv 
    ##### 

    ## merge two csv file
    def merge(self):
        dataframe11 = pd.read_csv(self.path1,sep=",")

        dataframe22 = pd.read_csv(self.path2,sep=",")


        df = pd.DataFrame()

        for i in range(28):
            df = dataframe11.iloc[:,i].append(dataframe22.iloc[:,i])

        df = pd.concat([dataframe11,dataframe22])
        df.to_csv(self.path1.replace('.csv', '_')+self.path2.replace('.csv', '_merged.csv'),index = None,header=None,float_format='%.4f')

        return self.path1.replace('.csv', '_')+self.path2.replace('.csv', '_merged.csv')


    # ## merge three csv file
    # def merge1(self):
    #
    #     dataframe11 = pd.read_csv(self.path1,sep=",")
    #
    #     dataframe22 = pd.read_csv(self.path2,sep=",")
    #
    #     dataframe33 = pd.read_csv(self.path3,sep=",")
    #
    #     whole_dataframe = dataframe11.append(dataframe22).append(dataframe33)
    #
    #     df = whole_dataframe.to_csv(self.path1.replace('.csv', '_')+self.path2.replace('.csv', '_')+self.path3.replace('.csv', '_merged.csv') ,index = None,header=None,float_format='%.4f')
    #
    #
    #
    # def merge2(self):
    #
    #     dataframe1111 = pd.read_csv(self.path1,sep=",")
    #
    #     dataframe2222 = pd.read_csv(self.path2,sep=",")
    #
    #     dataframe3333 = pd.read_csv(self.path3,sep=",")
    #
    #     dataframe4444 = pd.read_csv(self.path4,sep=",")
    #
    #     whole_dataframe = dataframe1111.append(dataframe2222).append(dataframe3333).append(dataframe4444)
    #
    #     df = whole_dataframe.to_csv(self.path1.replace('.csv', '_')+self.path2.replace('.csv', '_')+self.path3.replace('.csv', '_')+self.path4.replace('.csv', '_merged.csv') ,index = None,header=None,float_format='%.4f')



    def handle_nslkdd(self):
        nskkdd_dataframe = pd.read_csv(self.path3,sep=",")

        #adding title
        nskkdd_dataframe.columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins", "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_hot_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]

        #remove kdd redundant column
        
        nskkdd_dataframe = nskkdd_dataframe.drop(["hot","num_failed_logins", "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_hot_login","is_guest_login","difficulty"],axis=1)

    ####### change label name
        for i in range(len(nskkdd_dataframe)):
            if nskkdd_dataframe["label"][i] in ["back","land","neptune","pod","smurf","teardrop","mailbomb","processtable","udpstorm","apache2","worm"]:
                nskkdd_dataframe["label"][i] = "dos"
            elif nskkdd_dataframe["label"][i] in ["ipsweep","nmap","portsweep","satan","mscan","saint"]:
                nskkdd_dataframe["label"][i] = "scan"
            elif nskkdd_dataframe["label"][i] in ["ftp_write","guess_passwd","imap","multihop","phf","spy","warezclient","warezmaster","xlock","xsnoop","snmpguess","snmpgetattack","httptunnel","sendmail","named"]:
                nskkdd_dataframe["label"][i] = "r2l"
            elif nskkdd_dataframe["label"][i] in ["buffer_overflow","loadmodule","perl","rootkit","sqlattack","xterm","ps"]:
                nskkdd_dataframe["label"][i] = "u2r"
            else:
                nskkdd_dataframe["label"][i] = "normal"

        df = nskkdd_dataframe.to_csv(self.path3.replace('.csv', '_nslkdd_handled.csv') ,index = None)

        return self.path3.replace('.csv', '_nslkdd_handled.csv')

    #### to delete the str format header of csv


#
# if __name__ == '__main__':
#
#     mdh = My_data_handling()
#
#
#     path11 = "OSSSMOTEENN_AllData++.csv"
#     path22 = "NslKddTest_pre.csv"
#     merge(path11,path22)

