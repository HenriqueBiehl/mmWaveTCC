import numpy as np


def heuristic_scheduler(rate_u, status_u, allot_u, n, nts):
    X_res = np.zeros((n, nts))
    low_rate_user = np.empty(n) 
    low_rate_ts = np.empty(nts)
    rank_ts = np.empty(nts)

    for user in range(0, n):
        for ts in range(0, nts):
            low_rate_user[user] += status_u[user][ts]

    for ts in range(0, nts):
        for user in range(0, n):
            low_rate_ts[ts] += status_u[user][ts]
    
    rank_ts = np.argsort(low_rate_ts)[::-1]
    for ts in rank_ts: 
        assigned = 0 
        metric_u = low_rate_user + allot_u
        mask = allot_u > 0
        valid = np.where(mask)[0]
        rank_u = valid[np.argsort(valid)[::-1]]
        for user in rank_u:
            if (status_u[user][ts] == 0) and (allot_u[user] > 0):
                X_res[user][ts] = 1
                allot_u[user] = allot_u[user] - 1 

                for v in range(0, n):
                    low_rate_user[v] = low_rate_user[v] - status_u[v][ts]
                assigned = 1
            break 
        
        if assigned == 0:
            for user in rank_u:
                if allot_u[user] > 0:
                    X_res[user][ts] = 1
                    allot_u[user] = allot_u[user] - 1 
                    for v in range(0, n):
                        low_rate_user[v] = low_rate_user[v] - status_u[v][ts]
                break 
        

    return X_res
