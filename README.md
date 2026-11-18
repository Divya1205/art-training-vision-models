# Learning art by names or by looking

Code for a pilot study on how the training signal reshapes a vision model's view of art.

**Paper:** *Learning art by names or by looking: how the training signal reshapes a vision model's view of art.* Manuscript in preparation.

## What the study asks

Human art experts see abstract and representational art as more alike than novices do (Bimler et al., 2019). We asked whether the way a vision model learns about art changes how it organises paintings, and whether either way of learning moves it in that expert-like direction.

We took two vision models pretrained on large collections of general images and trained them further on paintings in two ways:

- **Labels:** the model learns to predict each painting's style (supervised).
- **Exposure:** the model gets no labels; it only learns that two different crops of the same painting belong together (self-supervised).

Then we compared each model with its own version before art training.

## Design

| | |
|---|---|
| Models | DINOv2-small (ViT-S/14) and DINOv3-small (ViT-S/16), both pretrained on natural images |
| Paintings | 960 from WikiArt, 120 from each of 8 styles: Impressionism, Baroque, Cubism, Ukiyo-e, Pop Art, Abstract Expressionism, Realism, Color Field Painting |
| Splits | 614 training, 154 validation, 192 test |
| Groups | *Abstract* = Abstract Expressionism + Color Field; *representational* = Baroque, Realism, Impressionism, Ukiyo-e; Cubism and Pop Art in-between. These are our own style-level choices, tested with alternative groupings. |
| Training | 30 epochs, 3-epoch head warm-up, gradient clipping, last 4 blocks at learning rate 3e-5. DINOv3 exposure used the last 8 blocks at 1e-4 so it changed as much as DINOv3 label training. |
| Seeds | 3 per condition |

## Main results (preliminary)

The analysis is still being revised; the manuscript will have the final numbers. In brief:

- **Labels** make style much easier to read out from the model and pull every style into a tight cluster, while adding little new style information. They push all styles apart, not abstraction specifically.
- **Exposure** spreads all paintings apart. On top of that spreading, pairs of styles that cross the abstract–representational divide move closer than their starting distance predicts. This holds on held-out test paintings, survives controls for simple image statistics (luminance, contrast, colour, edges, spatial frequency), and the real grouping is the most extreme of all 420 possible groupings of the styles.
- **A methods lesson:** group-level measures (centroid distance, and the pooled pairwise ratio) follow the general spread of the space, so painting-level, rank-based and spread-controlled measures are needed for claims like this.

## Limitations

- Small scale: 960 paintings, 8 styles, two small models from the same family, 3 seeds.
- The abstraction-specific convergence is small once general spreading is accounted for, and fails our strict pre-set rule (all four measures agreeing in every seed).
- Abstraction is labelled by style, not per painting.
- The exposure objective is SimCLR-style, not DINO's own training objective.
- These are results about models, not evidence about how people perceive art.

## Repository layout

```
notebooks/
  all_results.ipynb                          the one notebook: every result in the manuscript
                                             Part A  train all conditions and save embeddings (GPU)
                                             Part B  main analyses: probes, organisation, field, patches, four measures,
                                                     style pairs, groupings, maps, verdicts
                                             Part C  controls and null tests: test paintings only, centroid decomposition,
                                                     general spreading, exact nulls, image statistics
                                             Part D  style probes: accessibility vs presence, test-set intervals,
                                                     leakage-free few-shot probes
  supplementary/
    S1_robustness_checks.ipynb                earlier standalone robustness checks (now inside Part B)
    S2_warmup_dip_test.ipynb                  evidence that the early exposure dip was a head-initialisation artefact
    S3_exploration_attention_symmetry.ipynb   early exploration: attention maps, per-head changes, symmetry toy test
results/                                     saved embeddings are written here (not committed)
scripts/check_before_publish.py              scans the repository for secrets, notebook outputs and images
docs/PUBLISHING.md                           steps for publishing the repository safely
```

## Data

The paintings come from the WikiArt dataset as hosted on Hugging Face ([`huggan/wikiart`](https://huggingface.co/datasets/huggan/wikiart)), originally collected for the ArtGAN project (Tan et al., 2019). **This repository contains no images.** The notebooks stream the dataset and select the same 960 paintings every time (fixed shuffle seed 0). The dataset's licence is listed as unknown, and many modern works are under copyright, so do not redistribute the images.

## How to run

1. Open `notebooks/all_results.ipynb` in Google Colab with a **T4 GPU** (Kaggle has not been tested).
2. **For DINOv3**, request access on its [Hugging Face page](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m), create a read token, and add it as a secret named `HF_TOKEN`:
   key icon in the left sidebar in Colab, with notebook access switched on.

   Never paste the token into a code cell.
3. **Part A** trains all four conditions with three seeds (about 80–90 minutes on a T4) and saves each run to `RESULTS_DIR`. It skips runs already saved, so you can split it across sessions; set `RESULTS_DIR` to a Google Drive folder so results survive a disconnect.
4. **Parts B, C and D** produce every table and figure from the saved results, without a GPU: Part B in a few minutes, Parts C and D in about 20–25 minutes more (most of it tuning the MLP probe).

## Reproducibility

- **Seeds:** the painting sample uses shuffle seed 0 and split seed 0; each training run sets `torch`, `numpy` and `random` seeds (0, 1, 2) in `train_long`; UMAP and bootstrap use seed 0.
- **Software:** tested on Google Colab (Python 3.13) in October 2026. `requirements.txt` gives minimum versions; for exact versions see [docs/PUBLISHING.md](docs/PUBLISHING.md#pin-exact-versions).
- **Hardware:** one NVIDIA T4 (16 GB). DINOv3 runs in full precision because 16-bit precision overflows; DINOv2 uses mixed precision.

## Citation

See [`CITATION.cff`](CITATION.cff). Manuscript in preparation; citation details will be updated on publication.

## References

- Bimler, D. L., Snellock, M., & Paramei, G. V. (2019). Art expertise in construing meaning of representational and abstract artworks. *Acta Psychologica*, 192, 11–22.
- Tan, W. R., Chan, C. S., Aguirre, H. E., & Tanaka, K. (2019). Improved ArtGAN for conditional synthesis of natural image and artwork. *IEEE Transactions on Image Processing*, 28(1), 394–409.

## Licence

Code: [MIT](LICENSE). The licence covers the code only, not the WikiArt images or the pretrained model weights, which have their own terms.
