import const
import csv

FINISH_EPISODE = const.FINISH_EPISODE

class Log:    
    
    def __init__(self):
        pass
    
    def q_logger_step_episode(self,f): 
                
        data = [str(const.EPISODE_Agent1),str(const.Step_Agent1)]              
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(data)
        #if const.EPISODE_Agent1== FINISH_EPISODE:
            #self.f.close()
    
    
    def q_logger_q_table(self,qtable,row,col,action_count,q):
        
        for x in range(1,row):
            for y in range(1,col):
                for action in range(action_count):
 
                    data=[x,y,action,qtable[x][y][action]]
            
                    writer=csv.writer(q,lineterminator='\n')
                    writer.writerow(data)
        #self.q.close()
        
        #print('log OK!')
                    
    def q_logger_q_table_t(self,qtable,row,col,action_count):
        
        for x in range(1,row):
            for y in range(1,col):
                for action in range(action_count):
 
                    data=[x,y,action,qtable[x][y][action]]
            
                    writer=csv.writer(self.t,lineterminator='\n')
                    writer.writerow(data)
        #self.q.close()
        
        #print('log OK!')
    
    def boukyaku(self,episode,delta,b):
                            
        data=[episode,delta,1-delta]
        writer=csv.writer(b,lineterminator='\n')
        writer.writerow(data)
    
    def T_value(self,v):
        data = [str(const.EPISODE_Agent1),str(const.T)]              
        writer=csv.writer(v,lineterminator='\n')
        writer.writerow(data)
        
    def delta(self,delta,d,row,col):
        for x in range(1,row):
            for y in range(1,col):
                data = [x,y,delta[x][y]]
                writer=csv.writer(d,lineterminator='\n')
                writer.writerow(data)
        
        print("delta log ok")
        