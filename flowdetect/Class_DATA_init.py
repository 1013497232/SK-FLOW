import numpy as np
import pandas as pd
import csv
import math


class DATA_init:
    protocol_list = ['tcp', 'udp', 'icmp']

    flag_list = ['OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']

    service_list = ['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u',
                    'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest',
                    'hostnames',
                    'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell',
                    'ldap',
                    'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp',
                    'nntp',
                    'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje',
                    'shell',
                    'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time',
                    'urh_i', 'urp_i',
                    'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50', 'oth_i', 'smb', 'rdp']

    # 预处理，将文本中string内容替换为int
    def __init__(self, source_file):
        self.source_file = source_file
        self.pre_file = source_file.replace('.csv', '_pre.csv')
        self.standard_file = source_file.replace('.csv', '_standard.csv')
        self.standard_maxmin_file = source_file.replace('.csv', '_standard_maxmin.csv')
        self.row_num = 28

    def preHandel_data(self):
        data_file = open(self.pre_file, 'w', newline='')

        with open(self.source_file, 'r') as data_source:
            csv_reader = csv.reader(data_source)
            csv_writer = csv.writer(data_file)

            for row in csv_reader:
                temp_line = np.array(row)
                # 定义将源文件行中3种协议类型转换成数字标识的函数
                temp_line[1] = DATA_init.protocol_list.index(row[1])
                # 定义将源文件行中70种网络服务类型转换成数字标识的函数
                temp_line[2] = DATA_init.service_list.index(row[2])
                # 定义将源文件行中11种网络连接状态转换成数字标识的函数
                temp_line[3] = DATA_init.flag_list.index(row[3])
                csv_writer.writerow(temp_line)

        data_file.close()
        return self.pre_file

    # 数值标准化
    def Handle_data(self):
        data_file = open(self.standard_file, 'w', newline='')

        sum = np.zeros(self.row_num)  # 和
        sum.astype(float)
        avg = np.zeros(self.row_num)  # 平均值
        avg.astype(float)
        stadsum = np.zeros(self.row_num)  # 绝对误差
        stadsum.astype(float)
        stad = np.zeros(self.row_num)  # 平均绝对误差
        stad.astype(float)
        dic = {}
        lists = []

        for i in range(self.row_num):
            with open(self.source_file, 'r') as data_source:
                csv_reader = csv.reader(data_source)
                for row in csv_reader:
                    sum[i] += float(row[i])
            avg[i] = sum[i] / self.row_num  # 求每一列的平均值

            with open(self.source_file, 'r') as data_source:
                csv_reader = csv.reader(data_source)
                for row in csv_reader:
                    stadsum[i] += math.pow(abs(float(row[i]) - avg[i]), 2)
            stad[i] = stadsum[i] / self.row_num  # 求每一列的平均绝对误差

            with open(self.source_file, 'r') as data_source:
                csv_reader = csv.reader(data_source)
                list = []
                for row in csv_reader:
                    temp_line = np.array(row)  # 将每行数据存入temp_line数组里
                    if avg[i] == 0 or stad[i] == 0:
                        temp_line[i] = 0
                    else:
                        temp_line[i] = abs(float(row[i]) - avg[i]) / stad[i] # 标准值计算公式
                    list.append(temp_line[i])
                lists.append(list)

        with open(self.source_file, 'r') as data_source: #不对标签值进行处理，单独加入新的csv表格
            list = []
            csv_reader = csv.reader(data_source)
            for row in csv_reader:
                list.append(row[28])
            # print(list)
            lists.append(list)

        for j in range(len(lists)):
            dic[j] = lists[j]  # 将每一列的元素值存入字典中
        df = pd.DataFrame(data=dic)
        df.to_csv(data_file, index=False, header=False)
        data_file.close()
        return self.standard_file
    # 数值归一化
    def Find_Maxmin(self):
        dic = {}
        data_file = open(self.standard_maxmin_file, 'w', newline='')
        with open(self.source_file, 'r') as data_source:
            csv_reader = csv.reader(data_source)
            final_list = list(csv_reader)

            jmax = []
            jmin = []
            for k in range(len(final_list)):
                jmax.append(max(final_list[k][0:28]))
                jmin.append(min(final_list[k][0:28]))
            jjmax = float(max(jmax)) #找整体的最大值
            jjmin = float(min(jmin)) #找整体的最小值
            listss = []

            for i in range(self.row_num):
                lists = []
                with open(self.source_file, 'r') as data_source:
                    csv_reader = csv.reader(data_source)
                    for row in csv_reader:
                        if (jjmax - jjmin) == 0:
                            x = 0
                        else:
                            x = (float(row[i]) - jjmin) / (jjmax - jjmin) #归一值计算公式
                        lists.append(x)
                listss.append(lists)

            with open(self.source_file, 'r') as data_source: #不对标签值进行处理，单独加入新的csv表格
                lists = []
                csv_reader = csv.reader(data_source)
                for row in csv_reader:
                    lists.append(row[28])
                listss.append(lists)

            for j in range(len(listss)):
                dic[j] = listss[j]
            df = pd.DataFrame(data=dic)
            df.to_csv(data_file, index=False, header=False)

        data_file.close()
        return self.standard_maxmin_file

    # def solve(self, method=0): #method表示
