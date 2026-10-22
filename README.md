# AirCast India: AI Project Plan

**Week 1 Task - AI Project Planning and Documentation**

Author: Ansh Parashar

## Overview

AirCast India is a planned predictive analytics project that forecasts next-day PM2.5 concentration and air quality category for Indian cities using only publicly available datasets. This repository contains the complete project plan, the diagrams in it, and the scripts used to generate them.

This is a planning and feasibility deliverable. It defines what will be built and how success will be judged; it does not contain trained models or results.

## Main deliverable

- [`docs/AI_Project_Plan_AirCast_India.pdf`](docs/AI_Project_Plan_AirCast_India.pdf) - the full 9-page project plan (about 3,700 words).

## What the plan covers

1. Executive summary
2. Background and research (CRISP-DM, CRISP-ML(Q), Agile, forecasting literature)
3. Project objectives with measurable success criteria
4. Hypothesis formulation (H1-H5) with test methods
5. Tool and technology selection
6. Methodology for data collection and analysis
7. Model training and evaluation strategy
8. Data governance
9. Ethics and responsible AI
10. Scalability and deployment
11. Risks and mitigation (risk register)
12. Timeline and milestones (10-week Gantt chart)
13. Expected outcomes
14. Conclusion and references

## Planned data sources

- Central Pollution Control Board (CPCB) air-quality monitoring data
- ERA5 reanalysis weather data (Copernicus Climate Data Store)
- NASA FIRMS active-fire data

## Repository structure

```
.
├── docs/
│   └── AI_Project_Plan_AirCast_India.pdf   # final plan document
├── images/
│   ├── gantt.png                           # 10-week Gantt chart
│   └── workflow.png                        # end-to-end workflow diagram
├── scripts/
│   ├── diagrams.py                         # generates both diagrams
│   └── build_pdf.py                        # builds the PDF from the plan content
├── requirements.txt
└── README.md
```

## How the plan was built

The plan was written following CRISP-DM phase order with CRISP-ML(Q) style quality gates and weekly Agile increments. The diagrams are drawn with matplotlib and the document is assembled with ReportLab, so the whole deliverable is reproducible from code.

To regenerate it:

```bash
pip install -r requirements.txt
python scripts/diagrams.py     # writes images/gantt.png and images/workflow.png
python scripts/build_pdf.py    # writes docs/AI_Project_Plan_AirCast_India.pdf
```

## Timeline at a glance

| Milestone | Week | Deliverable |
|-----------|------|-------------|
| M1 Plan approved | End of W1 | Project plan, repository and environment |
| M2 Clean dataset | End of W3 | Validated multi-source dataset and data dictionary |
| M3 Baseline | End of W4 | Feature set v1 and baseline results |
| M4 Tuned model | End of W6 | Tuned LightGBM and LSTM experiments |
| M5 Prototype | End of W8 | Evaluation report, explainability, dashboard |
| M6 Final delivery | End of W10 | Final report, documented code, model card |

## License

Released under the MIT License. See [LICENSE](LICENSE).
