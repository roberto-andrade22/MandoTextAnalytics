import multiprocessing as mp
import time
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = '5120'
import torch
from get_plot import *
from  load_model import *

if __name__ == '__main__':
    mp.set_start_method('spawn')

    start = time.time()
    if torch.cuda.device_count() > 1:
        with mp.Pool(torch.cuda.device_count()) as pool:
            summaries_1 = []
            summaries_2 = []
            summaries_boba = []

            for summary in pool.map(make_episode_summary, season_one_episodes):
                summaries_1.append(summary)
                torch.cuda.empty_cache()
                gc.collect()

            for summary in pool.map(make_episode_summary, season_two_episodes):
                summaries_2.append(summary)
                torch.cuda.empty_cache()
                gc.collect()

            for summary in pool.map(make_episode_summary, boba_fett_episodes):
                summaries_boba.append(summary)
                torch.cuda.empty_cache()
                gc.collect()

    else:
        summaries_1 = []
        for episode in season_one_episodes:
            summary = make_episode_summary(episode)
            summaries_1.append(summary)
            torch.cuda.empty_cache()
            gc.collect()

        summaries_2 = []
        for episode in season_two_episodes:
            summary = make_episode_summary(episode)
            summaries_2.append(summary)
            torch.cuda.empty_cache()
            gc.collect()

        summaries_boba = []
        for episode in boba_fett_episodes:
            summary = make_episode_summary(episode)
            summaries_boba.append(summary)
            torch.cuda.empty_cache()
            gc.collect()         
 
    end = time.time()

    try:
        os.makedirs('../output')

    except FileExistsError:
        pass

    with open('../output/summaries.md', 'w') as f:
        f.write('# **Season 1** \n\n')
        for i,episode_summary in enumerate(summaries_1):
            f.write("### Chapter "+str(i+1)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/summaries.md', 'a') as f:
        f.write('\n# **Season 2** \n\n')
        for i, episode_summary in enumerate(summaries_2):
            f.write("### Chapter "+str(i+1+8)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/summaries.md', 'a') as f:
        f.write('\n# **The Book of Boba Fett** \n\n')
        for i, episode_summary in enumerate(summaries_boba):
            f.write("### Episode "+str(i+1)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/time_execution.txt','w') as f:
        s = "Total time of execution: " + str(round((end-start)/60,2)) + " minutes."
        f.write(s)
