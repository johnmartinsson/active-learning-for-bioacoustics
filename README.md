# A-CPD: From Weak to Strong Sound Event Labels using Adaptive Change-Point Detection and Active Learning

![Figure 2](results/figures/figure_2.png)

Official PyTorch implementation of the A-CPD method presented in the paper [From Weak to Strong Sound Event Labels using Adaptive Change-Point Detection and Active Learning](https://eurasip.org/Proceedings/Eusipco/Eusipco2024/pdfs/0000902.pdf), by [John Martinsson](https://johnmartinsson.org), [Olof Mogren](https://mogren.one), [Maria Sandsten](https://www.maths.lu.se/english/research/staff/mariasandsten/), and [Tuomas Virtanen](https://homepages.tuni.fi/tuomas.virtanen/)

[Paper](https://johnmartinsson.org/publications/2024/adaptive-change-point-detection) | [Data](https://zenodo.org/records/10811797)

Accepted for publication at EUSIPCO 2024 (and nominated as best student paper). For now, cite as:
    
    @misc{Martinsson2024,
          title={From Weak to Strong Sound Event Labels using Adaptive Change-Point Detection and Active Learning}, 
          author={John Martinsson and Olof Mogren and Maria Sandsten and Tuomas Virtanen},
          year={2024},
          eprint={2403.08525},
          archivePrefix={arXiv},
          primaryClass={cs.SD}
    }

## Just do it
Please read the doit.sh file. This command requires ~17GB of free disk space.

    bash doit.sh

This will reproduce all tables as standard output, and save all figures in

    './results/figures_reproduced'

If you are a bit more careful you could go through the doit.sh file and execute each command by itself.

## Reproduce figures and tables using reproduced experiment results

    bash doit.sh         # if you did not already run this    
    python src/main.py   # reproduce all simulated annotations

This will run all experiments presented in the paper and store the results in,

    ./results/eusipco_2024_reproduced

In the interest of time only 2 runs per configuration are done by default since the standard devaition is so low. All results should be similar, but may vary slightly.

Now update the src/config.py script and change to

    results_dir : eusipco_2024_reproduced

If you do not change this line, the produced figures and tables will be from the pre-computed eusipco_2024 results. Then run

    # produces all tables in the paper
    python src/tables.py

    # produces all figures in the paper
    python src/figures.py

## Reproduce figures and tables using reproduced audio mixture datasets
A description on how to download all the audio source material and how to use the scripts to generate the datasets and compute the embeddings using BirdNET will be made available upon demand. Please contact the main author of the paper.
