import numpy as np
import random
from Schedule import  Scheduling
from Machines import Machine_Time_window
from Jobs import Job
from Instance_8 import Processing_time,J,M_num,J_num,O_num
import matplotlib.pyplot as plt

class TACOSA:   #tuba-ant-colony-optimal-simulated annealing
    def __init__(self,J_num,O_num,M_num,alpha=2,beita=5,p=0.1,N_max=50,S=50,S_2=50,u=0.2):
        self.J_num=J_num        #工件总类
        self.O_total=O_num     #总工序数
        self.alpha=alpha        #信息素启发因子
        self.beita=beita        #期望启发因子
        self.p=p                #信息素蒸发率
        self.N_max=N_max        #最大迭代次数
        self.S=S                #第一层蚂蚁总数
        self.S_2=S_2
        self.Ant_Map=np.ones((J_num,O_num),dtype=float)    #第一阶段：工序排序蚂蚁地图
        self.Ant_Machine_Map=np.ones((O_num,M_num),dtype=float) #第二阶段：机器选择蚂蚁地图
        self.P0=0.1             #目前暂定为这样
        self.P1=0.6
        self.P2=0.7
    #候选集
    def Candidate_set(self,Jobs):  # 候选解集
        S_site=[]
        S_t0=[]
        priv_Job_O_num=0
        for i in range(len(Jobs)):
            if Jobs[i].Current_Processed()<Jobs[i].Operation_num:
                S_site.append(i)
                S_t0.append(self.Ant_Map[i,priv_Job_O_num+Jobs[i].Current_Processed()])
            priv_Job_O_num+=Jobs[i].Operation_num
        return S_t0,S_site

    def heur_info(self,Ealiest_time_Set,Ealiest):   #即为Nxy
        N=0
        for i in Ealiest_time_Set:
            N += 1 / (i + 1)
        return ((1 / (Ealiest + 1)) / N)

    #状态转移规则
    def State_trans_rule(self,Ealiest_Set,S_0):
        N_xy=[]     #工序启发式信息
        for i in Ealiest_Set:
            N_xy.append(self.heur_info(Ealiest_Set,i))
        Sum_t=0
        Argmax=[]
        for j in range(len(Ealiest_Set)):
            Sum_t+=S_0[j]**self.alpha*N_xy[j]**self.beita
            Argmax.append(S_0[j]**self.alpha*N_xy[j]**self.beita)
        Probis=[k/Sum_t for k in Argmax ]
        Sum_argmax=Probis.index(max(Probis))
        #选择下一步转移的节点
        roulette=[]     #装盘赌选择下一步转移节点
        lun=0
        roulette.append(lun)
        for A_i in Probis:
            lun+=A_i
            roulette.append(lun)
        q0=random.random()
        # print(q0)
        for r_i in range(len(roulette)):
            if roulette[r_i]>=q0:
                S=r_i-1
                break
        Site=S
        return Site

    def Operation_Site(self,J,Job,Operation):
        O_num=0
        for i in range(len(J)):
            if i==Job:
                return O_num+Operation
            else:
                O_num=O_num+J[i+1]

    #双向收敛策略：取目前调度时刻为止最好和部分最差路径，对其进行惩罚。
    #这是对第一层蚂蚁地图进行更新，即工序排序的更新
    def Bi_directional_convergence_strategy(self,Best,Ant,J,Wrost):
        #信息素挥发
        self.Ant_Map=self.Ant_Map*(1-self.p)
        self.Ant_Machine_Map=self.Ant_Machine_Map*(1-self.p)
        #信息素更新
        for i in range(len(Best)):
            Ant_i = Ant[Best[i][0]]
            Process_Sequence = Ant_i.Scheduled
            # print(Process_Sequence)
            Js = Ant_i.Jobs
            for S_i in range(len(Process_Sequence)):
                Machine = Js[Process_Sequence[S_i][0]].J_machine[Process_Sequence[S_i][1]]
                O_Site = self.Operation_Site(J, Process_Sequence[S_i][0], Process_Sequence[S_i][1])
                self.Ant_Map[Process_Sequence[S_i][0]][O_Site]  += (1 / Best[i][1])
                self.Ant_Machine_Map[O_Site][Machine]+= (1 / Best[i][1])
        for j in range(len(Wrost)):
            Ant_j=Ant[Wrost[j][0]]
            Process_Sequence=Ant_j.Scheduled
            for S_j in range(len(Process_Sequence)):
                O_Site = self.Operation_Site(J, Process_Sequence[S_j][0], Process_Sequence[S_j][1])
                self.Ant_Map[Process_Sequence[S_j][0]][O_Site] -=- (1 / Wrost[j][1])


    #寻找部分最优解和部分最劣解。
    def Select_Best_and_Worst_taril(self,Ant_fitness):
        Fit=[]
        for i in range(len(Ant_fitness)):
            Fit.append([i,Ant_fitness[i]])
        Fit=dict(Fit)
        Fit=sorted(Fit.items(),key=lambda x:x[1])
        eliest_num=int(0.2*self.S)
        Worst=Fit[-eliest_num:-1]
        Worst.append(Fit[-1])
        Best=Fit[0:eliest_num]
        return Best,Worst

    def Pair_Candidate_set(self,Job,O_num,Processing_time):
        workable_Machine=Processing_time[Job][O_num]
        Candidate=[]
        for i in range(len(workable_Machine)):
            if workable_Machine[i]!=9999:
                Candidate.append(i)
        return Candidate

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
                plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1])/2-0.5, y=i, s=Machine.assigned_task[i_1][0])
        plt.yticks(np.arange(i + 1), np.arange(1, i + 2))
        plt.title('Scheduling Gantt chart with double resource constraints')
        plt.ylabel('Machines')
        plt.xlabel('Time(s)')
        plt.show()

    #用作调试
    def Jobs_Situation(self,Jobs):
        for i in range(len(Jobs)):
            print(Jobs[i].Processed)

    #蚁群算法主程序
    def ACO_1(self, M_num, Processing_time,J):
        Set=[]
        Ant_best_fit=[]
        best_fit = 9999
        Best_Roat=None
        x=np.linspace(0,50,50)
        for i in range(self.N_max):
            Ant_roat=[]
            Ant_fitness=[]
            for j in range(self.S):
                Ant_Scheduling=\
                    Scheduling( M_num, Processing_time,J)
                J_s=Ant_Scheduling.Jobs         #工件集
                S_0=self.Candidate_set(J_s)
                while len(S_0[0]) >=1:
                    Ealiest_Set=[]          #最早开始时间集
                    for S_i in range(len(S_0[0])):
                        Job=S_0[1][S_i]
                        O_i=Ant_Scheduling.Jobs[Job].Current_Processed()
                        Pair_candidate=self.Pair_Candidate_set(Job,O_i,Processing_time)
                        Time_Candidate=[]
                        Time_Candidate_2=[]
                        P=[]#以机器负荷作为信息引导
                        Pair_ant_info=[]
                        for M_i in Pair_candidate:
                            Time_Candidate.append(Processing_time[Job][O_i][M_i])
                            Time_Candidate_2.append(Ant_Scheduling.Machines[M_i].Machine_Burden())
                            Pair_ant_info.append(self.Ant_Machine_Map[self.Operation_Site(J, Job, O_i)][M_i])
                        if  random.random()>self.P2:
                            Pair_Site = self.State_trans_rule(Time_Candidate_2, Pair_ant_info)
                        else:
                            Pair_Site=self.State_trans_rule(Time_Candidate,Pair_ant_info)
                        Machine=Pair_candidate[Pair_Site]
                        Ealiest_i = Ant_Scheduling.Earliest_Start(Job,O_i,Machine) #基于工人负荷选择最合适的机器
                        Ealiest_Set.append(Ealiest_i)
                    #基于最早开始时间选择
                    Job_Ealiest_Start_Set=[]
                    for E_i in range(len(Ealiest_Set)):
                            Job_Ealiest_Start_Set.append(Ealiest_Set[E_i][0])
                    Job_Site=self.State_trans_rule(Job_Ealiest_Start_Set,S_0[0])
                    Seleted_Job=S_0[1][Job_Site]
                    Para=Ealiest_Set[Job_Site]
                    Ant_Scheduling.add_job(Seleted_Job,Para[0],Para[1],Para[2],Para[3],Para[5],Para[6])
                    S_0 = self.Candidate_set(J_s)
                Ant_roat.append(Ant_Scheduling)
                fitness= Ant_Scheduling.fitness
                Ant_fitness.append(fitness)
            Trail_Situation=self.Select_Best_and_Worst_taril(Ant_fitness)
            Best=Trail_Situation[0]
            Worst=Trail_Situation[1]
            self.Bi_directional_convergence_strategy(Best, Ant_roat,J,Worst)
            Best_Ant=Trail_Situation[0][0]
            Set.append(Ant_roat[Best[0][0]])
            # print(Best[0][1])
            if Best[0][1]<best_fit:
                best_fit=Best[0][1]
                # print(Best[0][1])
                Best_Roat=Ant_roat[Best[0][0]]
            Ant_best_fit.append(best_fit)
        plt.plot(x,Ant_best_fit,'-k')
        plt.title('the maximum completion time of each iteration for dual resource constrained flexible job shop scheduling problem')
        plt.ylabel('Cmax')
        plt.xlabel('Test Num')
        plt.show()
        self.Gantt(Best_Roat.Machines)
        return Ant_best_fit[-1]

    def ACO_2(self, M_num, Processing_time,J):
        Set=[]
        Ant_best_fit=[]
        best_fit = 9999
        Best_Roat=None
        x=np.linspace(0,50,50)
        for i in range(self.N_max):
            Ant_roat=[]
            Ant_fitness=[]
            for j in range(self.S):
                Ant_Scheduling=\
                    Scheduling( M_num, Processing_time,J)
                Ant_Scheduling2 = \
                    Scheduling(M_num, Processing_time, J)
                Ant_Scheduling3 = \
                    Scheduling(M_num, Processing_time, J)
                J_s=Ant_Scheduling.Jobs         #工件集
                S_0=self.Candidate_set(J_s)
                while len(S_0[0]) >=1:
                    Ealiest_Set=[]          #最早开始时间集
                    for S_i in range(len(S_0[0])):
                        Job=S_0[1][S_i]
                        O_i=Ant_Scheduling.Jobs[Job].Current_Processed()
                        Pair_candidate=self.Pair_Candidate_set(Job,O_i,Processing_time)
                        Time_Candidate=[]
                        Time_Candidate_2=[]
                        P=[]#以机器负荷作为信息引导
                        Pair_ant_info=[]
                        for M_i in Pair_candidate:
                            Time_Candidate.append(Processing_time[Job][O_i][M_i])
                            Time_Candidate_2.append(Ant_Scheduling.Machines[M_i].Machine_Burden())
                            Pair_ant_info.append(self.Ant_Machine_Map[self.Operation_Site(J, Job, O_i)][M_i])
                        if  random.random()>self.P2:
                            Pair_Site = self.State_trans_rule(Time_Candidate_2, Pair_ant_info)
                        else:
                            Pair_Site=self.State_trans_rule(Time_Candidate,Pair_ant_info)
                        Machine=Pair_candidate[Pair_Site]
                        Ealiest_i = Ant_Scheduling.Earliest_Start_Insert(Job,O_i,Machine) #基于工人负荷选择最合适的机器
                        Ealiest_Set.append(Ealiest_i)
                    #基于最早开始时间选择
                    Job_Ealiest_Start_Set=[]
                    for E_i in range(len(Ealiest_Set)):
                            Job_Ealiest_Start_Set.append(Ealiest_Set[E_i][0])
                    Job_Site=self.State_trans_rule(Job_Ealiest_Start_Set,S_0[0])
                    Seleted_Job=S_0[1][Job_Site]
                    Para=Ealiest_Set[Job_Site]
                    Ant_Scheduling.add_job(Seleted_Job,Para[0],Para[1],Para[2],Para[3],Para[5],Para[6])
                    S_0 = self.Candidate_set(J_s)
                Ant_roat.append(Ant_Scheduling)
                fitness= Ant_Scheduling.fitness
                Ant_fitness.append(fitness)
            Trail_Situation=self.Select_Best_and_Worst_taril(Ant_fitness)
            Best=Trail_Situation[0]
            Worst=Trail_Situation[1]
            self.Bi_directional_convergence_strategy(Best, Ant_roat,J,Worst)
            Best_Ant=Trail_Situation[0][0]
            Set.append(Ant_roat[Best[0][0]])
            # print(Best[0][1])
            if Best[0][1]<best_fit:
                best_fit=Best[0][1]
                # print(Best[0][1])
                Best_Roat=Ant_roat[Best[0][0]]
            Ant_best_fit.append(best_fit)
        plt.plot(x,Ant_best_fit,'-k')
        plt.title('the maximum completion time of each iteration for dual resource constrained flexible job shop scheduling problem')
        plt.ylabel('Cmax')
        plt.xlabel('Test Num')
        plt.show()
        self.Gantt(Best_Roat.Machines)
        return Ant_best_fit[-1]

    def ACO_3(self, M_num, Processing_time,J):
        Set=[]
        Ant_best_fit=[]
        best_fit = 9999
        Best_Roat=None
        x=np.linspace(0,30,30)
        for i in range(self.N_max):
            Ant_roat=[]
            Ant_fitness=[]
            for j in range(self.S):
                Ant_Scheduling=\
                    Scheduling( M_num, Processing_time,J)
                J_s=Ant_Scheduling.Jobs         #工件集
                S_0=self.Candidate_set(J_s)
                while len(S_0[0]) >=1:
                    Ealiest_Set=[]          #最早开始时间集
                    for S_i in range(len(S_0[0])):
                        Job=S_0[1][S_i]
                        O_i=Ant_Scheduling.Jobs[Job].Current_Processed()
                        Pair_candidate=self.Pair_Candidate_set(Job,O_i,Processing_time)
                        Time_Candidate=[]
                        Time_Candidate_2=[]
                        P=[]#以机器负荷作为信息引导
                        Pair_ant_info=[]
                        for M_i in Pair_candidate:
                            Time_Candidate.append(Processing_time[Job][O_i][M_i])
                            Time_Candidate_2.append(Ant_Scheduling.Machines[M_i].Machine_Burden())
                            Pair_ant_info.append(self.Ant_Machine_Map[self.Operation_Site(J, Job, O_i)][M_i])
                        if  random.random()>self.P2:
                            Pair_Site = self.State_trans_rule(Time_Candidate_2, Pair_ant_info)
                        else:
                            Pair_Site=self.State_trans_rule(Time_Candidate,Pair_ant_info)
                        Machine=Pair_candidate[Pair_Site]
                        Ealiest_i = Ant_Scheduling.Earliest_Start_NOt_Insert(Job,O_i,Machine) #基于工人负荷选择最合适的机器
                        Ealiest_Set.append(Ealiest_i)
                    #基于最早开始时间选择
                    Job_Ealiest_Start_Set=[]
                    for E_i in range(len(Ealiest_Set)):
                            Job_Ealiest_Start_Set.append(Ealiest_Set[E_i][0])
                    Job_Site=self.State_trans_rule(Job_Ealiest_Start_Set,S_0[0])
                    Seleted_Job=S_0[1][Job_Site]
                    Para=Ealiest_Set[Job_Site]
                    Ant_Scheduling.add_job(Seleted_Job,Para[0],Para[1],Para[2],Para[3],Para[5],Para[6])
                    S_0 = self.Candidate_set(J_s)
                Ant_roat.append(Ant_Scheduling)
                fitness= Ant_Scheduling.fitness
                Ant_fitness.append(fitness)
            Trail_Situation=self.Select_Best_and_Worst_taril(Ant_fitness)
            Best=Trail_Situation[0]
            Worst=Trail_Situation[1]
            self.Bi_directional_convergence_strategy(Best, Ant_roat,J,Worst)
            Best_Ant=Trail_Situation[0][0]
            Set.append(Ant_roat[Best[0][0]])
            # print(Best[0][1])
            if Best[0][1]<best_fit:
                best_fit=Best[0][1]
                # print(Best[0][1])
                Best_Roat=Ant_roat[Best[0][0]]
            Ant_best_fit.append(best_fit)
        plt.plot(x,Ant_best_fit,'-k')
        plt.title('the maximum completion time of each iteration for dual resource constrained flexible job shop scheduling problem')
        plt.ylabel('Cmax')
        plt.xlabel('Test Num')
        plt.show()
        self.Gantt(Best_Roat.Machines)
        return Ant_best_fit[-1]

ac=TACOSA(J_num,O_num,M_num)
x=np.linspace(0,10,10)
EST=[]      #
ECT=[]      #最早完工
MIX=[]      #混合随机
for i in range(10):
    A_1=ac.ACO_1(M_num,Processing_time, J)
    EST.append(A_1)
    # A_2 = ac.ACO_2(M_num,Processing_time, J)
    # ECT.append(A_2)
    # A_3= ac.ACO_3(M_num,Processing_time, J)
    # MIX.append(A_3)
fig=plt.figure()
plt.plot(x,EST,'-k',label='EST')
plt.plot(x,ECT,'-.k',label='ECT')
plt.plot(x,MIX,':k',label='MIX')
plt.title('Different machine worker selection strategies')
plt.ylabel('Cmax')
plt.xlabel('Test Num')
plt.legend(["Machine selection based on worker load","Selecting workers based on machine load","MIX"])
plt.show()
