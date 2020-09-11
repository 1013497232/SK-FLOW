import time
import pandas as pd
from sklearn.model_selection import train_test_split
from flowdetect import myKnn, mySVC, MyLogiRe, myRf, myVoting, myStacking, vis, data_handling, handle_imbalance
from flowdetect.Class_DATA_init import DATA_init

print('------------------Welcome--------------------')
while (True):
    print('选择要进行的操作：')
    print('\t1.预处理数据集')
    print('\t2.训练模型')
    print('\t3.用已有模型进行测试')
    print('\t4.预测流量类型')
    print('\t其他字符.退出')
    choice = int(input())

    if choice == 1:
        print('是否需要进行预处理：')
        print('\t0.是')
        print('\t1.否')
        pre_method = int(input())

        if pre_method == 0:
            print('请选择需要的预处理：')

            print('\t0.处理kdd99原生数据')
            print('\t1.处理生成器生成后添加标签的数据')
            print('\t2.处理NslKdd原生数据')
            print('\t3.合并操作')
            pre_method1 = int(input())

            if pre_method1 == 0:
                print('选择要进行的数据操作的原始数据集：')
                file_path = str(input())
                data_format = data_handling.data_handling(path1=file_path)
                output_path = data_format.handle_kdd99()
                output_path = data_handling.delete_first_line(output_path)
                output_path = data_handling.reindex(output_path)

                data = DATA_init(output_path)
                output_path = data.preHandel_data()

                print("成功输出预处理文件：" + output_path)

            elif pre_method1 == 1:
                print('选择要进行的数据操作的原始数据集：')
                file_path = str(input())
                data_format = data_handling.data_handling(path2=file_path)
                output_path = data_format.handle_new()
                output_path = data_handling.delete_first_line(output_path)
                output_path = data_handling.reindex(output_path)

                data = DATA_init(output_path)
                output_path = data.preHandel_data()

                print("成功输出预处理文件：" + output_path)


            elif pre_method1 == 2:
                print('选择要进行的数据操作的原始数据集：')
                file_path = str(input())
                data_format = data_handling.data_handling(path3=file_path)
                output_path = data_format.handle_nslkdd()
                output_path = data_handling.delete_first_line(output_path)
                output_path = data_handling.reindex(output_path)

                data = DATA_init(output_path)
                output_path = data.preHandel_data()
                print("成功输出预处理文件：" + output_path)

            elif pre_method1 == 3:

                print('选择前一个有表头数据集：')
                file_path1 = str(input())
                print('选择后一个有表头数据集：')
                file_path2 = str(input())
                data_format = data_handling.data_handling(path1=file_path1, path2=file_path2)
                output_path = data_format.merge()
                print("成功输出无表头文件：" + output_path)


        elif pre_method == 1:
            print("将直接进入数据处理部分，之后的文件请选择已经预处理的文件")

        print('选择要进行的数据操作：')
        print('\t0.增广')
        print('\t1.标准化')
        print('\t2.归一化')
        method = int(input())

        print('选择要进行的数据操作的数据集：')

        file_path = str(input())

        if method == 0:
            dhi = handle_imbalance.handle_imbalance(file_path)
            output_path = dhi.use_OSSSMOTEENN()
            print("成功输出增广文件：" + output_path)
        elif method == 1:
            data = DATA_init(file_path)
            output_path = data.Handle_data()
            print("成功输出标准化文件：" + output_path)

        elif method == 2:

            data = DATA_init(file_path)
            output_path = data.Find_Maxmin()
            print("成功输出归一化文件：" + output_path)

    # DATA_init.solve(DATA, choice1)
    # continue

    elif choice == 2 or choice == 3 or choice == 4:
        print('选择数据集：')
        file_path = str(input())
        file = pd.read_csv(file_path)

        print('选择要使用的模型：')
        print('\t1.KNN算法')
        print('\t2.支持向量机算法')
        print('\t3.逻辑回归算法')
        print('\t4.随机森林算法')
        print('\t5.投票器')
        print('\t6.堆叠')
        print('\t7.数据可视化展示')
        choice2 = int(input())

        # 训练模型
        if choice == 2:
            data_feature = file.iloc[:, 0:28]
            data_label = file.iloc[:, 28]
            x_train, x_test, y_train, y_test = train_test_split(data_feature, data_label, test_size=0.2)
            if choice2 == 1:
                study = myKnn.myKnn(x_train, y_train, x_test, y_test, False)
            elif choice2 == 2:
                study = mySVC.mySVC(x_train, y_train, x_test, y_test, False)
            elif choice2 == 3:
                study = MyLogiRe.MyLogiRe(x_train, y_train, x_test, y_test, False)
            elif choice2 == 4:
                study = myRf.myRf(x_train, y_train, x_test, y_test, False)
            elif choice2 == 5:
                study = myVoting.myVoting(x_train, y_train, x_test, y_test, False)
            elif choice2 == 6:
                study = myStacking.myStacking(x_train, y_train, x_test, y_test, False)
            elif choice == 7:
                v = vis.vis(x_test, y_test)
                v.solve()
                exit(1)
            else:
                print("Wrong number!")
                exit(1)

            start_time = time.time()
            study.excute()
            end_time = time.time()
            print("total time:%.2fs" % (end_time - start_time))

        # 用已有模型进行测试
        elif choice == 3:
            x_test = file.iloc[:, 0:28]
            y_test = file.iloc[:, 28]
            if choice2 == 1:
                study = myKnn.myKnn(None, None, x_test, y_test, True)
            elif choice2 == 2:
                study = mySVC.mySVC(None, None, x_test, y_test, True)
            elif choice2 == 3:
                study = MyLogiRe.MyLogiRe(None, None, x_test, y_test, True)
            elif choice2 == 4:
                study = myRf.myRf(None, None, x_test, y_test, True)
            elif choice2 == 5:
                study = myVoting.myVoting(None, None, x_test, y_test, True)
            elif choice2 == 6:
                study = myStacking.myStacking(None, None, x_test, y_test, True)
            elif choice2 == 7:
                v = vis.vis(x_test, y_test)
                v.solve()
                exit(1)
            else:
                print("Wrong number!")
                exit(1)

            study.excute()

        # 用已有模型预测数据包类型
        elif choice == 4:
            x_test = file.iloc[:, 0:28]
            if choice2 == 1:
                study = myKnn.myKnn(None, None, x_test, None, True)
            elif choice2 == 2:
                study = mySVC.mySVC(None, None, x_test, None, True)
            elif choice2 == 3:
                study = MyLogiRe.MyLogiRe(None, None, x_test, None, True)
            elif choice2 == 4:
                study = myRf.myRf(None, None, x_test, None, True)
            elif choice2 == 5:
                study = myVoting.myVoting(None, None, x_test, None, True)
            elif choice2 == 6:
                study = myStacking.myStacking(None, None, x_test, None, True)
            elif choice2 == 7:
                print("这是预测功能，请使用2或者3功能得到可视化结果")
                exit(1)
            else:
                print("Wrong number!")
                exit(1)

            study.predict()
    else:
        break
