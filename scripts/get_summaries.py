import multiprocessing as mp
import time
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = '1024'
import torch
from get_plot import *
from  load_model import *

def summarize_episodes(episodes):
    summaries = []
    for episode in episodes:
        summary = make_episode_summary(episode)
        summaries.append(summary)
        torch.cuda.empty_cache()
    return summaries

if __name__ == '__main__':
    mp.set_start_method('spawn')
    season_one_episodes = get_season_plot(season_one)
    season_two_episodes = get_season_plot(season_two)

    start = time.time()
    if torch.cuda.device_count() > 1:
        with mp.Pool(torch.cuda.device_count()) as pool:
            summaries_1 = []
            summaries_2 = []
            for summary in pool.imap(make_episode_summary, season_one_episodes):
                summaries_1.append(summary)
                torch.cuda.empty_cache()

            for summary in pool.imap(make_episode_summary, season_two_episodes):
                summaries_2.append(summary)
                torch.cuda.empty_cache()
    else:
        summaries_1 = []
        for episode in season_one_episodes:
            summary = make_episode_summary(episode)
            summaries_1.append(summary)
            torch.cuda.empty_cache()

        summaries_2 = []
        for episode in season_two_episodes:
            summary = make_episode_summary(episode)
            summaries_2.append(summary)
            torch.cuda.empty_cache()
 
    end = time.time()

    try:
        os.makedirs('../output')

    except FileExistsError:
        pass

    with open('../output/season_one.md', 'w') as f:
        f.write('Season 1:\n\n')
        for i,episode_summary in enumerate(summaries_1):
            f.write("Episode "+str(i+1)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/season_two.md', 'w') as f:
        f.write('Season 2:\n\n')
        for i, episode_summary in enumerate(summaries_2):
            f.write("Episode "+str(i+1+8)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/time_execution.txt','w') as f:
        s = "Total time of execution: " + str(round((end-start)/60,2)) + " minutes."
        f.write(s)
