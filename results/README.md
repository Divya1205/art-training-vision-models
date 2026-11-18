# results/

`notebooks/all_results.ipynb` (Part A) saves its training results here (or in the folder set as `RESULTS_DIR`):

- `<model>__before.npz`: embeddings of all 960 paintings before art training
- `<model>__before_spatial.json`: patch-structure measures before training
- `<model>__<objective>_s<seed>.npz`: embeddings at every recorded epoch for one run
- `<model>__<objective>_s<seed>.json`: final patch-structure measures and settings for that run

These files are not committed (they are large and can be regenerated). Part B of the notebook needs only these files.
