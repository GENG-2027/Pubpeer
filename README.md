# Pubpeer
 **This repository contains a reproducible numerical examination of the filled points displayed in Fig. 5 of Wang et al., *Nature Biomedical Engineering*, DOI: 10.1038/s41551-026-01666-y. The materials document the published figure, the associated Source Data, and an independent reconstruction of the plotted performance coordinates.**


- **`Figure_A_published_Fig5.png`**  
  Crop of the published Fig. 5 from the article. The labels **“Dots: individual participant”** and **“n = 216”** are highlighted to document how the filled points are described in the published figure.

- **`Figure_B_published_SourceData_Fig5.png`**  
  Visual transcription of the two worksheets in the published Fig. 5 Source Data file (`Top1` and `map`). It shows that the workbook contains five numerical values per model for each metric rather than participant-level values corresponding to the filled points in Fig. 5.

- **`Figure_C_reconstruction_evidence.png`**  
  Numerical reconstruction evidence. The upper panel compares the first 90 NeuroSTORM Top-1 values extracted from the PDF with the fixed-seed reconstruction. The lower panel shows the absolute discrepancies for all 6,400 filled points.

- **`fig5_6400_point_comparison.csv`**  
  Point-by-point comparison for all 6,400 filled markers extracted from Fig. 5. Each row contains the metric, model, point order, PDF-derived performance value, fixed-seed reconstructed value, and residual.

- **`fig5_group_summary.csv`**  
  Summary statistics for the 16 model/metric groups. Includes the reconstruction centre, number of plotted points, maximum and median absolute discrepancy, and Pearson correlation between the PDF-derived and reconstructed values.

- **`fig5_published_source_data_transcription.csv`**  
  Exact tabular transcription of the published Fig. 5 Source Data workbook, including both the `Top1` and `map` worksheets.

- **`fig5_reconstruction_check.py`**  
  Standalone Python script that independently extracts the filled vector markers from the published PDF, calibrates the performance axes, reconstructs the values using the fixed NumPy random sequence, and reports the numerical agreement.


