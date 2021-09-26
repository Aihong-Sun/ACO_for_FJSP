import decimal
from Jobs import Job
from Machines import Machine_Time_window
import numpy as np
import random
import matplotlib.pyplot as plt


class Scheduling:
    def __init__(self, M_num, Processing_time,J):
        self.Processing_time = Processing_time
        self.Scheduled = []                 #已经排产过的工序
        self.M_num = M_num
        self.Machines = []  # 存储机器类
        self.fitness=0
        for j in range(M_num):
            self.Machines.append(Machine_Time_window(j))
        self.Machine_State = np.zeros(M_num, dtype=int)  # 在机器上加工的工件是哪个
        self.Jobs = []
        for k, v in J.items():
            self.Jobs.append(Job(k, v))

    def Earliest_Start1(self, Job, O_num, Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()
        M_Tstart = M_window[0]
        M_Tend = M_window[1]
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        Forced_Insertion = 0
        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start = M_Tstart[le_i]
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        ealiest_start = last_O_end
                        break
                #     if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t * 0.6 and M_Tlen[
                #         le_i] - last_O_end < P_t:
                #         ealiest_start = last_O_end
                #         Forced_Insertion = 1
                #         break
                #     break
                # if M_Tlen[le_i] >= P_t * 0.6 and M_Tlen[le_i] < P_t:
                #     if M_Tstart[le_i] >= last_O_end:
                #         ealiest_start = M_Tstart[le_i]
                #         Forced_Insertion = 1
                #         break
                #     if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t * 0.6:
                #         ealiest_start = last_O_end
                #         Forced_Insertion = 1
                #         break
                #     break
        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t
        return M_Ealiest, Selected_Machine, P_t, O_num, End_work_time, Forced_Insertion, last_O_end

    def Earliest_Start2(self, Job, O_num, Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()
        M_Tstart = M_window[0]
        M_Tend = M_window[1]
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        Forced_Insertion = 0
        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start = M_Tstart[le_i]
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        if M_Tlen-P_t>6:
                            ealiest_start = M_Tend[le_i]-P_t
                        else:
                            ealiest_start = last_O_end
                        break
                        #     if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t * 0.6 and M_Tlen[
                        #         le_i] - last_O_end < P_t:
                        #         ealiest_start = last_O_end
                        #         Forced_Insertion = 1
                        #         break
                        #     break
                        # if M_Tlen[le_i] >= P_t * 0.6 and M_Tlen[le_i] < P_t:
                        #     if M_Tstart[le_i] >= last_O_end:
                        #         ealiest_start = M_Tstart[le_i]
                        #         Forced_Insertion = 1
                        #         break
                        #     if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t * 0.6:
                        #         ealiest_start = last_O_end
                        #         Forced_Insertion = 1
                        #         break
                        #     break
        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t
        return M_Ealiest, Selected_Machine, P_t, O_num, End_work_time, Forced_Insertion, last_O_end


    def Earliest_Start(self,Job,O_num,Machine):
        P_t=self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine=Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()
        M_Tstart = M_window[0]
        M_Tend = M_window[1]
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        Forced_Insertion=0
        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start=M_Tstart[le_i]
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        ealiest_start = last_O_end
                        break
                    if M_Tstart[le_i]<last_O_end and M_Tend[le_i]-last_O_end>=P_t*0.6 and M_Tlen[le_i]-last_O_end<P_t :
                        ealiest_start=last_O_end
                        Forced_Insertion=1
                        break
                    break
                if M_Tlen[le_i]>=P_t*0.6 and M_Tlen[le_i]<P_t:
                    if M_Tstart[le_i]>=last_O_end :
                        ealiest_start = M_Tstart[le_i]
                        Forced_Insertion = 1
                        break
                    if M_Tstart[le_i]<last_O_end and M_Tend[le_i]-last_O_end>=P_t*0.6:
                        ealiest_start = last_O_end
                        Forced_Insertion = 1
                        break
                    break
        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t
        return M_Ealiest, Selected_Machine, P_t, O_num, End_work_time,Forced_Insertion,last_O_end

    def Earliest_Start_Insert(self,Job,O_num,Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()
        M_Tstart = M_window[0]
        M_Tend = M_window[1]
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        Forced_Insertion = 0
        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start = M_Tstart[le_i]
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        ealiest_start = last_O_end
                        break
        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t
        return M_Ealiest, Selected_Machine, P_t, O_num, End_work_time, Forced_Insertion, last_O_end

    def Earliest_Start_NOt_Insert(self,Job,O_num,Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        Forced_Insertion = 0
        M_Ealiest = ealiest_start
        End_work_time = M_Ealiest + P_t
        return M_Ealiest, Selected_Machine, P_t, O_num, End_work_time, Forced_Insertion, last_O_end

    #判断强迫插入影响到的工序
    def Influenced_Operation(self,Machine,Job,P_t,O_num,ealiest_start,last_o_end):
        End_time=self.Machines[Machine].O_end
        Start_time=self.Machines[Machine].O_start
        Influend=[]
        for i in range(len(Start_time)):
            if ealiest_start<Start_time[i]:
                back_off = ealiest_start + P_t - Start_time[i ]
                for j in range(i,len(Start_time)-1):
                        Influend.append(self.Machines[Machine].assigned_task[j])
                        Start_time[j]+=back_off
                        End_time[j]+=back_off
                # self.Machines[Machine].O_end=End_time
                # self.Machines[Machine].O_start=Start_time
                # self.Machines[Machine]._Input(Job, ealiest_start, P_t, O_num)
                # End=ealiest_start+P_t
                # self.Jobs[Job]._Input(ealiest_start, End, Machine)
                break
        for k in range(len(Influend)):
            J_num=Influend[k][0]-1
            J=self.Jobs[Influend[k][0]-1]
            O_i=J.Current_Processed()
            if O_i==Influend[k][1]:
                pass
            else:
                for k_1 in range(Influend[k][1],O_i):
                    # print(k_1)
                    Machine_J=J.J_machine[k_1]
                    if Machine_J==Machine:
                        pass
                    else:
                        Site=self.Machines[Machine_J].assigned_task.index([Influend[k][0],k_1+1])
                        for S_i in range(Site,len(self.Machines[Machine_J].O_start)):
                            self.Machines[Machine_J].O_start[S_i]+=back_off
                            self.Machines[Machine_J].O_end[S_i] += back_off
                    self.Jobs[Influend[k][0] - 1].J_start[k_1]+=back_off
                    self.Jobs[Influend[k][0]-1].J_end[k_1]+=back_off
        self.Machines[Machine].O_end = End_time
        self.Machines[Machine].O_start = Start_time
        self.Machines[Machine]._Input(Job, ealiest_start, P_t, O_num)
        End = ealiest_start + P_t
        self.Jobs[Job]._Input(ealiest_start, End, Machine)

    def add_job(self,Job,M_Ealiest,Selected_Machine,P_t,O_num,Force_Insertion,last_o_end):
        if Force_Insertion==0:
            self.Scheduled.append([Job,O_num])
            self.Machines[Selected_Machine]._Input(Job,M_Ealiest,P_t,O_num)
            End_time=M_Ealiest+P_t
            self.Jobs[Job]._Input(M_Ealiest,End_time,Selected_Machine)
            if self.fitness<End_time:
                self.fitness=End_time
        else:
            try:
                self.Influenced_Operation(Selected_Machine,Job,P_t,O_num,M_Ealiest,last_o_end)
            except:
                self.Gantt(self.Machines)
                print(Job,M_Ealiest,P_t,O_num)

    def Gantt(self,Machines):
        M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
             'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
             'navajowhite',
             'navy', 'sandybrown', 'moccasin']
        for i in range(len(Machines)):
            Machine=Machines[i]
            Start_time=Machine.O_start
            End_time=Machine.O_end
            for i_1 in range(len(End_time)):
                # plt.barh(i,width=End_time[i_1]-Start_time[i_1],height=0.8,left=Start_time[i_1],\
                #          color=M[Machine.assigned_task[i_1][0]],edgecolor='black')
                # plt.text(x=Start_time[i_1]+0.1,y=i,s=Machine.assigned_task[i_1])
                plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1], \
                         color='white', edgecolor='black')
                s = Machine.assigned_task[i_1]
                plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1])/2-0.5, y=i, s=Machine.assigned_task[i_1])
        plt.yticks(np.arange(i + 1), np.arange(1, i + 2))
        plt.title('Scheduling Gantt chart ')
        plt.ylabel('Machines')
        plt.xlabel('Time(s)')
        plt.show()

if __name__=='__main__':
    M=3
    J={1:3,2:4,3:3}
    Processing_time=[[
        [1,2,3],
        [1.3,4],
        [3,2,5]
    ],
    [
        [1,3,4],
        [2,3,4],
        [2,5,3],
        [4,3,5]
    ],
    [
        [1,3,4],
        [4,4,5],
        [3,2,5]
    ]]
    S=Scheduling(M,Processing_time,J)
    S.Jobs[1].J_start=[0]
    S.Jobs[1].J_end=[1]

    S.Jobs[0]._Input(0, 1, 0)
    S.Machines[0]._Input(0,0,1,0)

    S.Jobs[1]._Input(1, 2, 0)
    S.Machines[0]._Input(1, 1, 1, 0)

    S.Jobs[1]._Input(2, 5, 1)
    S.Machines[1]._Input(1, 2, 3, 1)

    S.Jobs[1]._Input(5, 7, 0)
    S.Machines[0]._Input(1, 5, 2, 2)

    S.Jobs[0]._Input(7, 8, 0)
    S.Machines[0]._Input(0, 7, 1, 1)

    S.Jobs[0]._Input(8, 10, 1)
    S.Machines[1]._Input(0, 8, 2, 2)

    S.Gantt(S.Machines)
    P=S.Earliest_Start(2,0,1)
    S.add_job(2,P[0],P[1],P[2],P[3],P[5],P[6])
    S.Gantt(S.Machines)

    P = S.Earliest_Start(2, 1, 0)
    S.add_job(2, P[0], P[1], P[2], P[3], P[5], P[6])
    S.Gantt(S.Machines)





