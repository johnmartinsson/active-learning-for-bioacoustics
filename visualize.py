import os
import librosa
import numpy as np
from scipy.signal import find_peaks, peak_widths

import matplotlib.pyplot as plt

import utils
import datasets
import oracles
import query_strategies as qs
import change_point_detection as cpd

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def visualize_query_strategy(query_strategy, query_strategy_name, soundscape_basename, base_dir, n_queries=7, vis_probs=True, vis_queries=True, vis_threshold=True, vis_cpd=True, vis_label=True, vis_peaks=True, savefile=None):
    oracle = oracles.WeakLabelOracle(base_dir)
    
    timings, embeddings = datasets.load_timings_and_embeddings(base_dir, soundscape_basename)
    pred_probas = query_strategy.predict_probas(embeddings)
    pred_queries = query_strategy.predict_queries(soundscape_basename, n_queries=n_queries)
    pred_pos_events = oracle.pos_events_from_queries(pred_queries, soundscape_basename)
    ts_probas = np.mean(timings, axis=1)

    soundscape_length = qs.get_soundscape_length(base_dir, soundscape_basename)
    opt_queries = qs.optimal_query_strategy(base_dir, soundscape_basename, soundscape_length)
    ref_pos_events = oracle.pos_events_from_queries(opt_queries, soundscape_basename)

    # extract Mel spectrogram
    window_length = 0.025
    wave, sr = librosa.load(os.path.join(base_dir, soundscape_basename + ".wav"))
    mel_spectrogram = librosa.feature.melspectrogram(
        y=wave,
        sr=sr,
        n_fft = utils.next_power_of_2(int(sr * window_length)),
        hop_length = utils.next_power_of_2(int(sr * window_length)) // 2,
    )
    
    fig, ax = plt.subplots(2, 1, figsize=(10,3.0))
    ax[0].imshow(np.flip(np.log(mel_spectrogram + 1e-10), axis=0), aspect='auto')
    ax[0].set_title("Method: {}".format(query_strategy_name))
    ax[0].set_xticklabels([])
    ax[0].set_yticklabels([])

    probas = pred_probas.reshape((len(pred_probas), 1))
    ds = cpd.distance_past_and_future_averages(
        probas,
        cpd.euclidean_distance_score, offset=0, M=1
    )

    # peaks 
    peaks = find_peaks(ds, prominence=0)
    peak_indices     = peaks[0]
    peak_prominences = peaks[1]['prominences']
    peak_indices = sorted(utils.sort_by_rank(peak_prominences, peak_indices)[:n_queries-1])

    if vis_peaks:
        ax[1].plot(ts_probas[peak_indices], ds[peak_indices], "x", color="red")

    if vis_cpd:
        ax[1].plot(ts_probas, ds, label='cpd', color=colors[0])
    if vis_probs:
        ax[1].plot(ts_probas, pred_probas, label='probas', color=colors[1])
    if vis_threshold:
        ax[1].hlines([0.5], [0], [soundscape_length], color='red', linestyle='dashed')
    ax[1].set_xlim(0, soundscape_length) #ts_probas[-1])
    ax[1].set_ylim(0, 1.2)
    ax[1].set_xlabel('time [s]')
    ax[1].set_ylabel('pseudo-probability')

    def plot_events(ax, events, color, label, ymax=1.0):
        starts = [s for (s, _) in events]
        ends   = [e for (_, e) in events]
        heights = [ymax for _ in range(len(events))]
        ax.vlines(starts + ends, ymin=0, ymax=ymax, color=color, label=label)
        ax.hlines(heights, starts, ends, color=color)

    def plot_queries(ax, queries, color, label):
        points = [e for (s, e) in queries]
        points = [0.1] + points + [29.9]
        ax.vlines(points, ymin=-0.2, ymax=1.2, color=color, label=label, linestyle='dashed')

    # plot true event onsets and offsets
    plot_events(ax[1], ref_pos_events, color='green', label='reference labels', ymax=0.9)
    if vis_label:
        plot_events(ax[1], pred_pos_events, color='magenta', label='annotated labels', ymax=0.95)

    if vis_queries:
        #plot_queries(ax[1], opt_queries, color='green', label='reference queries')
        plot_queries(ax[1], pred_queries, color='magenta', label='predicted queries')

        query_centers = [e - ((e - s) / 2) for (s, e) in pred_queries]
        for idx_q_c, q_c in enumerate(query_centers):
            ax[1].text(x=q_c-0.3, y=1.05, s=r'$q_{}$'.format(idx_q_c))
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()

    if savefile is not None:
        plt.savefig(savefile, bbox_inches='tight')
        #plt.cla()
        #plt.clf()
        #plt.close()
