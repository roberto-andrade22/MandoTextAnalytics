import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = '5120'
import torch
from get_plot import *
from  load_model import *

if __name__ == '__main__':
    season_one_episodes = get_season_plot(season_one)
    season_two_episodes = get_season_plot(season_two)

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

    try:
        os.makedirs('../output')

    except FileExistsError:
        pass

    with open('../output/summaries.md', 'w') as f:
        f.write('# **Season 1** \n\n')
        for i,episode_summary in enumerate(summaries_1):
            f.write("### Episode "+str(i+1)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/summaries.md', 'a') as f:
        f.write('\n# **Season 2** \n\n')
        for i, episode_summary in enumerate(summaries_2):
            f.write("### Episode "+str(i+1+8)+":\n")
            f.write(episode_summary)
            f.write('\n\n')

    with open('../output/summaries.md', 'a') as f:
        f.write('\n# **The Book of Boba Fett** \n\n')
        for i, episode_summary in enumerate(summaries_boba):
            f.write("### Episode "+str(i+1)+":\n")
            f.write(episode_summary)
            f.write('\n\n')