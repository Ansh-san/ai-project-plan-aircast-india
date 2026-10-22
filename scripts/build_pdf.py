from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table,
                                TableStyle, Image, KeepTogether, ListFlowable, ListItem)

import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(BASE, "images") + os.sep
OUT = os.path.join(BASE, "docs", "AI_Project_Plan_AirCast_India.pdf")

ss = getSampleStyleSheet()
NAVY = colors.HexColor("#1f4e79")
body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=10.2, leading=14.1,
                      alignment=TA_JUSTIFY, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19,
                    textColor=NAVY, spaceBefore=12, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                    textColor=colors.HexColor("#2e75b6"), spaceBefore=8, spaceAfter=3)
title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=26, leading=32,
                       textColor=NAVY, alignment=0, spaceAfter=8)
sub = ParagraphStyle("sub", parent=body, fontSize=13, leading=18, alignment=0, textColor=colors.HexColor("#444444"))
cap = ParagraphStyle("cap", parent=body, fontSize=8.8, leading=12, alignment=0, textColor=colors.HexColor("#555555"),
                     spaceAfter=10)
cell = ParagraphStyle("cell", parent=body, fontSize=8.6, leading=11.4, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)

story = []
P = lambda t, s=body: story.append(Paragraph(t, s))
H1 = lambda t: story.append(Paragraph(t, h1))
H2 = lambda t: story.append(Paragraph(t, h2))


def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, body), leftIndent=14) for i in items],
                              bulletType="bullet", start="•", leftIndent=14, bulletFontSize=9))


def table(rows, widths, header=True):
    data = []
    for r_i, r in enumerate(rows):
        data.append([Paragraph(c, cellb if (header and r_i == 0) else cell) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        for i in range(1, len(rows)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f2f6fa")))
    t.setStyle(TableStyle(st))
    story.append(t)
    story.append(Spacer(1, 8))


# ---------------- Cover ----------------
story.append(Spacer(1, 3.5 * cm))
P("AI Project Plan and Documentation", title)
P("AirCast India: Next-Day PM2.5 and Air Quality Category Forecasting Using Publicly Available Datasets", sub)
story.append(Spacer(1, 0.6 * cm))
P("Week 1 Task - Predictive Analytics Project Planning, Feasibility Assessment and Documentation", sub)
story.append(Spacer(1, 1.2 * cm))
table([["Document type", "Project plan (ideation, planning and feasibility)"],
       ["Project domain", "Environmental predictive analytics (time-series forecasting and classification)"],
       ["Planned duration", "10 weeks (single practitioner, part-time equivalent of roughly 20 hours per week)"],
       ["Data sources", "CPCB air-quality monitoring data, ERA5 reanalysis weather data, NASA FIRMS active-fire data"],
       ["Prepared by", "Ansh Parashar"],
       ["Prepared", "October 2026"]], [4.2 * cm, 12.3 * cm], header=False)
story.append(Spacer(1, 1 * cm))
P("<b>Contents.</b> 1 Executive summary; 2 Background and research; 3 Objectives; 4 Hypotheses; "
  "5 Tools and technology; 6 Methodology; 7 Model training and evaluation; 8 Data governance; "
  "9 Ethics and responsible AI; 10 Scalability; 11 Challenges and risk mitigation; 12 Timeline and milestones; "
  "13 Expected outcomes; 14 Conclusion; References.", body)
story.append(PageBreak())

# ---------------- 1 Executive summary ----------------
H1("1. Executive Summary")
P("Air pollution is one of the most significant public-health problems in India, and fine particulate matter "
  "(PM2.5) is the pollutant most strongly associated with respiratory and cardiovascular illness. Citizens, schools "
  "and local authorities routinely make decisions - whether to hold outdoor events, when to restrict construction, "
  "when to issue health advisories - that would benefit from a reliable forecast of tomorrow's air quality rather "
  "than only a report of today's. This project, called <b>AirCast India</b>, plans the design, development and "
  "evaluation of a predictive analytics system that forecasts next-day average PM2.5 concentration, and the "
  "corresponding air quality category, for a set of Indian cities using only publicly available datasets.")
P("This document is the planning artefact for the project. It does not report results; it defines what will be "
  "built, why, with which tools, by which method, in what order, and how success and failure will be recognised. "
  "It covers objectives, testable hypotheses, technology selection, data collection and analysis methodology, model "
  "training and evaluation strategy, data governance, ethical considerations, scalability, a risk register with "
  "mitigations, a ten-week timeline with a Gantt chart and milestones, and the expected outcomes. The plan "
  "deliberately balances theory (established practice in time-series forecasting and in the CRISP-DM process) with "
  "practical execution (concrete tools, weekly deliverables, and explicit acceptance criteria).")

# ---------------- 2 Background ----------------
H1("2. Background and Research Summary")
H2("2.1 Predictive analytics in context")
P("Predictive analytics uses historical data and statistical or machine learning models to estimate the value or "
  "class of a future outcome. For air quality, the target is a variable that changes over time and depends on "
  "emissions, meteorology and geography, so the problem is best framed as supervised learning on time-series data. "
  "Two framings are used in this plan. The first is <i>regression</i>: predict the numeric daily mean PM2.5 for "
  "tomorrow. The second is <i>ordinal classification</i>: predict the air quality category (for example Good, "
  "Satisfactory, Moderate, Poor, Very Poor, Severe) used in India's national air quality index. Regression gives "
  "precision, while classification matches how people actually consume the information.")
H2("2.2 Planning methodologies reviewed")
P("Three methodologies informed the plan. <b>CRISP-DM</b> (Cross-Industry Standard Process for Data Mining) "
  "describes six iterative phases: business understanding, data understanding, data preparation, modelling, "
  "evaluation and deployment. It is widely used because it keeps technical work tied to a stated purpose. "
  "<b>CRISP-ML(Q)</b> extends this with quality assurance activities and an explicit monitoring and maintenance "
  "phase, which matters here because air quality patterns drift with policy, season and sensor changes. "
  "<b>Agile delivery</b> contributes short iterations, weekly deliverables and early baselines, so that problems "
  "surface in week four rather than week nine. The plan therefore follows the CRISP-DM phase order, adds "
  "CRISP-ML(Q) style quality gates and monitoring, and is scheduled in weekly increments.")
H2("2.3 Technical literature reviewed")
P("Published work on air quality forecasting consistently reports four findings that shape the design. First, "
  "persistence (tomorrow equals today) is a surprisingly strong baseline for daily PM2.5, so any complex model must "
  "be compared against it. Second, gradient-boosted decision trees on lagged and meteorological features are "
  "competitive with deep sequence models on modest data volumes while being cheaper and easier to interpret. "
  "Third, meteorological variables such as boundary-layer height, wind speed and temperature, together with "
  "regional biomass-burning indicators, add predictive value beyond the pollutant history. Fourth, random "
  "train-test splits leak future information in time-series work, so chronological validation is essential. "
  "These findings lead directly to the baseline-first, tree-model-first, chronologically-validated approach "
  "described below, with a recurrent neural network included as a secondary experiment rather than an assumption.")

# ---------------- 3 Objectives ----------------
H1("3. Project Objectives")
P("The primary objective is to build and rigorously evaluate a model that forecasts next-day mean PM2.5 for "
  "selected Indian cities more accurately than a persistence baseline, using only open data. The objectives below "
  "are written to be specific and measurable so that completion can be judged objectively.")
table([["ID", "Objective", "Measure of success"],
       ["O1", "Assemble a clean, documented, reproducible multi-source dataset for at least 8 Indian cities covering "
              "a minimum of five years of daily observations.",
        "Dataset with data dictionary; missingness report; documented provenance and licence for each source."],
       ["O2", "Establish credible baselines (persistence, seasonal naive, linear model).",
        "Baseline results on a held-out chronological test set, logged and reproducible."],
       ["O3", "Train and tune at least two advanced models (gradient boosting and a recurrent network).",
        "Best model reduces RMSE by at least 15 percent against persistence on the test period."],
       ["O4", "Classify next-day air quality category with useful accuracy.",
        "Macro-averaged F1 of at least 0.60 and within-one-category accuracy of at least 90 percent."],
       ["O5", "Explain model behaviour and verify fairness of performance across cities.",
        "Feature-importance and SHAP analysis; per-city error report with no city exceeding 1.5 times the median RMSE "
        "without a documented explanation."],
       ["O6", "Deliver a working prototype dashboard and complete documentation.",
        "Interactive dashboard showing forecast, uncertainty and model caveats; final report and code repository."]],
      [1.1 * cm, 8.2 * cm, 7.2 * cm])
P("The numerical targets are planning assumptions grounded in the literature rather than guarantees. If early "
  "experiments show that they are unrealistic, they will be revised at the Milestone M3 review with the reasoning "
  "documented, rather than silently relaxed.")

# ---------------- 4 Hypotheses ----------------
H1("4. Hypothesis Formulation")
P("Hypotheses turn vague expectations into claims that data can support or refute. Each hypothesis below states a "
  "null and an alternative form, and each will be tested on the chronological test set using paired comparisons of "
  "forecast errors, with bootstrap confidence intervals over test days.")
table([["ID", "Hypothesis", "How it will be tested"],
       ["H1", "A model using lagged PM2.5 and meteorological features forecasts next-day PM2.5 with lower RMSE than "
              "persistence. (Null: no difference.)",
        "Paired bootstrap of daily squared-error differences; report mean improvement and 95 percent interval."],
       ["H2", "Adding meteorological variables (wind, temperature, humidity, boundary-layer height) improves accuracy "
              "over a pollutant-history-only model.",
        "Ablation study: identical model with and without weather feature group."],
       ["H3", "Adding satellite-derived fire counts improves forecasts in the post-monsoon crop-residue burning "
              "season for northern cities.",
        "Seasonal ablation restricted to October-November test days for northern cities."],
       ["H4", "Gradient-boosted trees perform at least as well as an LSTM network on this data volume.",
        "Same features and splits; compare RMSE, training cost and calibration."],
       ["H5", "Model error is not uniformly distributed: coastal cities are forecast more accurately than "
              "northern plain cities.",
        "Per-city and per-season error decomposition; Kruskal-Wallis test across city groups."]],
      [1.1 * cm, 8.4 * cm, 7.0 * cm])

# ---------------- 5 Tools ----------------
H1("5. Tool and Technology Selection")
P("Tool choices favour open-source, widely documented software that a single practitioner can run on a laptop or "
  "a free cloud notebook, which keeps the project reproducible and inexpensive. Each choice is justified against "
  "an alternative that was considered.")
table([["Area", "Selected tool", "Rationale and alternative considered"],
       ["Language and environment", "Python 3.11 with Jupyter and a pinned virtual environment",
        "Dominant data science ecosystem; R is capable but offers fewer deployment options."],
       ["Data handling", "pandas, NumPy, pyarrow (Parquet storage)",
        "Parquet is compact and typed; avoids repeated CSV parsing errors."],
       ["Geospatial and weather", "xarray, netCDF4, geopandas",
        "ERA5 data are distributed as gridded netCDF; xarray handles labelled arrays natively."],
       ["Modelling", "scikit-learn, LightGBM, PyTorch",
        "scikit-learn for baselines and pipelines; LightGBM for fast tree boosting; PyTorch for the LSTM experiment."],
       ["Tuning and tracking", "Optuna and MLflow",
        "Optuna provides efficient Bayesian search; MLflow records parameters, metrics and artefacts for reproducibility."],
       ["Explainability", "SHAP and partial dependence plots",
        "Model-agnostic and well suited to tree ensembles."],
       ["Visualisation and dashboard", "matplotlib, Plotly, Streamlit",
        "Streamlit allows a prototype dashboard in pure Python; a full web stack is out of scope."],
       ["Version control and quality", "Git and GitHub, pytest, pre-commit",
        "Enables review history, automated data-validation tests and consistent formatting."],
       ["Data validation", "Pandera (or Great Expectations)",
        "Declarative schema and range checks that run at ingestion."]],
      [3.3 * cm, 5.0 * cm, 8.2 * cm])
story.append(Image(D + "workflow.png", width=16.5 * cm, height=16.5 * cm * 0.255))
P("Figure 1. End-to-end workflow from public data sources to dashboard, with a feedback loop for drift detection "
  "and retraining.", cap)

# ---------------- 6 Methodology ----------------
H1("6. Methodology for Data Collection and Analysis")
H2("6.1 Data sources")
P("Three complementary public sources will be used. <b>Air-quality observations</b> come from the Central "
  "Pollution Control Board's continuous monitoring network, accessed through the national open data portal and "
  "through widely used compiled versions of the same data. These provide daily or hourly PM2.5, PM10, NO2, SO2, "
  "CO and ozone readings by station and city. <b>Weather data</b> come from ERA5, the global atmospheric "
  "reanalysis produced by the European Centre for Medium-Range Weather Forecasts and distributed free through the "
  "Copernicus Climate Data Store. Variables include temperature, wind components, relative humidity, "
  "precipitation and boundary-layer height. <b>Fire activity</b> comes from NASA FIRMS active-fire detections, "
  "which will be aggregated into counts within a fixed radius of each region. Before use, the licence and "
  "attribution terms of each source will be checked and recorded in the data catalogue.")
H2("6.2 Data collection and ingestion")
P("Ingestion will be scripted rather than manual, so that every step can be rerun. Raw files will be stored "
  "unmodified in an immutable raw layer, then converted to typed Parquet in a processed layer. Each ingestion run "
  "writes a manifest recording the source URL, retrieval date, file hash and row count. Automated schema checks "
  "reject files with unexpected columns, impossible values (for example negative concentrations) or timestamps "
  "outside the expected range.")
H2("6.3 Exploratory analysis and cleaning")
P("Exploratory analysis will quantify missingness by station and year, examine distributions and outliers, "
  "decompose series into trend, seasonality and residual, and inspect autocorrelation. Short gaps of up to three "
  "days will be filled by time-aware interpolation, and each imputed value will be flagged with an indicator "
  "feature so that the model and the evaluation can tell observed from inferred data. Longer gaps will not be "
  "imputed; stations with excessive missingness will be excluded, and the exclusion rule will be written down "
  "before looking at model results to avoid selecting data that flatters the model. Station readings will be "
  "aggregated to a city-day mean with a minimum number of contributing stations.")
H2("6.4 Feature engineering")
P("Features will be grouped so that ablation studies are straightforward. The <i>history group</i> contains "
  "lagged PM2.5 for one to seven days, rolling means and standard deviations, and the difference from the "
  "previous day. The <i>meteorology group</i> contains same-day and forecast-relevant weather variables and their "
  "lags. The <i>fire group</i> contains regional fire counts with short lags. The <i>calendar group</i> contains "
  "day of week, month, harmonic seasonal terms and a festival-period indicator. A strict rule applies to every "
  "feature: it may use only information that would have been available at the moment the forecast is made. "
  "Leakage tests in the automated suite will verify this by shifting data and confirming performance does not "
  "improve implausibly.")
H2("6.5 Analysis approach")
P("Analysis proceeds from simple to complex. Descriptive statistics and correlation analysis establish which "
  "variables are related to PM2.5; baselines establish the bar to beat; and advanced models are accepted only if "
  "they beat that bar by a margin larger than the uncertainty of the estimate. All random processes use fixed "
  "seeds, and results are reported as means with intervals over repeated runs where randomness is involved.")

# ---------------- 7 Model training and evaluation ----------------
H1("7. Model Training and Evaluation Strategy")
H2("7.1 Data splitting and validation")
P("Data will be split chronologically: the earliest roughly 70 percent for training, the next 15 percent for "
  "validation and the most recent 15 percent as a final test set that is touched only once, at the end of "
  "model selection. Hyperparameter tuning will use expanding-window (rolling-origin) cross-validation within "
  "the training period, which respects temporal order and mimics how the model would be used in practice. A "
  "gap of one day between training and validation windows will prevent leakage through autocorrelation.")
H2("7.2 Models")
bullets(["<b>Persistence and seasonal naive:</b> the minimum standard every other model must beat.",
         "<b>Regularised linear regression (Ridge):</b> an interpretable benchmark showing how much is explained "
         "by simple linear relationships.",
         "<b>LightGBM gradient boosting:</b> the expected primary model, tuned with Optuna over learning rate, "
         "tree depth, number of leaves, regularisation and feature sampling.",
         "<b>LSTM sequence model (PyTorch):</b> a secondary experiment using a window of recent days, trained with "
         "early stopping and dropout to control overfitting.",
         "<b>Quantile regression variants:</b> to produce prediction intervals so that the dashboard can express "
         "uncertainty rather than a single number."])
H2("7.3 Evaluation metrics")
P("Regression quality will be measured with RMSE, MAE and the coefficient of determination, plus mean "
  "absolute scaled error (MASE) to compare against the naive forecast on a common scale. Classification quality "
  "will be measured with macro-F1, per-class recall and the confusion matrix, with particular attention to the "
  "recall of the 'Poor' and worse categories, because failing to warn of a severe day is costlier than a false "
  "alarm. Calibration of prediction intervals will be checked by comparing nominal and observed coverage. "
  "Performance will always be reported overall and broken down by city and by season.")
H2("7.4 Error analysis and robustness")
P("Beyond aggregate scores, the largest forecast errors will be reviewed case by case to find systematic causes, "
  "such as festival-related spikes, missing fire data or sensor faults. Robustness will be probed by adding noise "
  "to inputs, removing feature groups, and testing on a held-out city that the model never saw in training, which "
  "gives an honest indication of how well the approach generalises to new locations.")

# ---------------- 8 Data governance ----------------
H1("8. Data Governance")
P("Although all sources are public, good governance still applies. The project will maintain a <b>data "
  "catalogue</b> listing each dataset's owner, licence, retrieval date, update frequency, known quality issues "
  "and permitted uses. <b>Lineage</b> will be preserved so that every figure in the final report can be traced "
  "to a specific raw file and code version. <b>Quality controls</b> are automated at ingestion and tested in "
  "continuous integration. <b>Access and storage</b> follow the principle of least privilege: credentials and "
  "API keys are kept in environment variables and never committed to the repository. <b>Retention and "
  "reproducibility</b> are served by storing raw data hashes and environment lock files. Because the data "
  "describe the environment rather than individuals, personal-data risk is low; nevertheless, if any future "
  "extension introduces location traces or health records, a privacy impact assessment will be required before "
  "use, consistent with India's Digital Personal Data Protection Act, 2023.")

# ---------------- 9 Ethics ----------------
H1("9. Ethical Considerations and Responsible AI")
bullets(["<b>Fairness of coverage:</b> monitoring stations are concentrated in large cities, so smaller towns and "
         "poorer neighbourhoods are under-represented. The report will state this limitation clearly and will avoid "
         "claiming that the model applies where there is no monitoring.",
         "<b>Consequences of errors:</b> a missed severe-pollution day can lead people to be exposed unknowingly. "
         "Thresholds will therefore favour recall for dangerous categories, and the dashboard will show uncertainty "
         "and advise users to consult official advisories.",
         "<b>Transparency and explainability:</b> SHAP analysis, model cards and a plain-language description of "
         "limitations will accompany any released model.",
         "<b>Honest reporting:</b> negative results, failed hypotheses and weak cities will be reported, not hidden.",
         "<b>Appropriate use:</b> the system is an educational and decision-support prototype, not an official "
         "forecast, and must not replace statutory air-quality bulletins.",
         "<b>Environmental cost:</b> models are deliberately small, and compute use will be logged, in keeping with "
         "the project's environmental theme."])

# ---------------- 10 Scalability ----------------
H1("10. Scalability and Deployment Considerations")
P("The prototype targets eight cities, but the design anticipates growth. Data pipelines are written as "
  "parameterised functions keyed by city, so adding a city means adding a configuration entry rather than "
  "writing new code. Parquet partitioning by city and year supports efficient reads as data volumes grow. "
  "Training cost is dominated by hyperparameter search, which parallelises naturally across Optuna trials and "
  "could move to a cloud batch service if the city count reaches the hundreds. For serving, a trained model is "
  "small enough to be wrapped in a lightweight API container and called once per day by a scheduled job, which "
  "avoids the cost and complexity of real-time infrastructure. Monitoring will track input distribution drift "
  "and rolling forecast error against realised observations, with a retraining trigger when error exceeds a set "
  "tolerance for several consecutive weeks. Moving from a prototype to production would additionally require "
  "service-level objectives, alerting, access control and a formal review of the ethical points above.")

# ---------------- 11 Risks ----------------
H1("11. Potential Challenges and Risk Mitigation")
P("The risk register below ranks each risk by likelihood and impact (Low, Medium, High) and assigns a "
  "preventive action and a contingency. It will be reviewed at every weekly checkpoint.")
table([["Risk", "Likelihood / Impact", "Mitigation (prevent)", "Contingency (respond)"],
       ["Missing or inconsistent station data", "High / High",
        "Early missingness audit; strict station inclusion rules; imputation flags.",
        "Reduce the city set; use city-level aggregation; document exclusions."],
       ["Data leakage inflating results", "Medium / High",
        "Chronological splits; leakage tests; features limited to forecast-time information.",
        "Re-run all experiments after fixing; report original and corrected scores."],
       ["Source access or format changes", "Medium / Medium",
        "Cache raw files with hashes; scripted ingestion; mirror source documentation.",
        "Fall back to the compiled archival dataset for the affected period."],
       ["Models fail to beat persistence", "Medium / Medium",
        "Baseline-first plan; focus on feature quality; early review at M3.",
        "Reframe as a diagnostic study of why predictability is limited; still deliver findings."],
       ["Concept drift (policy, sensors, seasons)", "Medium / Medium",
        "Test on the latest period; rolling-origin validation; drift monitoring.",
        "Retrain on recent window; widen intervals."],
       ["Scope creep and schedule slippage", "High / Medium",
        "Fixed milestones; MoSCoW prioritisation; two buffer days per phase.",
        "Drop the LSTM experiment and dashboard extras before dropping evaluation rigour."],
       ["Insufficient compute", "Low / Medium",
        "Lightweight models; subsampled tuning; free notebook GPU for the LSTM only.",
        "Reduce tuning trials; use smaller windows."],
       ["Ethical misuse or over-trust", "Low / High",
        "Clear caveats; uncertainty display; model card.",
        "Restrict distribution to the report; withdraw dashboard if misuse is identified."]],
      [3.6 * cm, 2.5 * cm, 5.4 * cm, 5.0 * cm])

# ---------------- 12 Timeline ----------------
H1("12. Timeline and Milestones")
P("The project runs for ten weeks. Phases overlap deliberately where one can start before the previous one "
  "fully finishes, for example feature engineering beginning while cleaning is completed, but no phase starts "
  "before its inputs are validated. Figure 2 shows the Gantt chart, and the table that follows defines the "
  "deliverable and acceptance criterion for each milestone.")
story.append(Image(D + "gantt.png", width=16.5 * cm, height=16.5 * cm * 1120 / 2200))
P("Figure 2. Ten-week Gantt chart with six milestones (red diamonds mark the end of the stated week).", cap)
table([["Milestone", "Week", "Deliverable", "Acceptance criterion"],
       ["M1 Plan approved", "End of W1", "This project plan; repository and environment set up.",
        "Plan reviewed; objectives and hypotheses agreed."],
       ["M2 Clean dataset", "End of W3", "Validated, documented multi-source dataset and data dictionary.",
        "All schema tests pass; missingness report completed."],
       ["M3 Baseline", "End of W4", "Feature set v1 and baseline model results.",
        "Persistence and linear baselines logged; go/no-go review of targets."],
       ["M4 Tuned model", "End of W6", "Tuned LightGBM and LSTM with experiment history in MLflow.",
        "Validation results reproducible from a single command."],
       ["M5 Prototype", "End of W8", "Evaluation report, explainability outputs and working dashboard.",
        "Final test set scored once; ethics checklist completed."],
       ["M6 Final delivery", "End of W10", "Final report, documented code and model card.",
        "All objectives assessed against stated measures."]],
      [2.9 * cm, 2.0 * cm, 6.2 * cm, 5.4 * cm])
P("Effort is budgeted at about twenty hours per week, with the heaviest load in weeks five to seven during model "
  "training and evaluation. Each phase includes a two-day buffer. If a milestone is at risk, the contingency "
  "order is fixed in advance: first cut optional experiments, then dashboard polish, and only last any element of "
  "evaluation or documentation, because credibility depends on them.")

# ---------------- 13 Outcomes ----------------
H1("13. Expected Outcomes and Success Criteria")
P("The project is expected to produce five tangible outputs. First, a reproducible dataset and data pipeline "
  "covering multiple cities and sources. Second, a benchmarked set of models with a clear statement of how much "
  "predictive value is added over persistence. Third, evidence for or against each hypothesis, including "
  "findings that may be negative. Fourth, an explainability and fairness analysis showing which factors drive "
  "forecasts and where the model is weak. Fifth, a prototype dashboard and a complete documentation set, so that "
  "another practitioner could reproduce and extend the work.")
P("Success is defined in layers. <b>Minimum success</b> is a clean dataset, valid baselines and an honest "
  "evaluation, even if advanced models offer only small gains. <b>Target success</b> is meeting objectives O1 "
  "to O6, including a 15 percent RMSE improvement over persistence. <b>Stretch success</b> adds accurate "
  "calibrated intervals, strong performance on an unseen city and a documented path to daily automated "
  "operation. The layered definition keeps the project valuable even if the data prove harder than expected, "
  "since a rigorous demonstration of a predictability limit is itself a useful result.")

# ---------------- 14 Conclusion ----------------
H1("14. Conclusion")
P("AirCast India is a feasible, well-scoped predictive analytics project: the data are open, the tools are free, "
  "the compute needs are modest and the timeline contains explicit milestones and buffers. Its design reflects "
  "good practice in AI project planning - a clear problem statement, falsifiable hypotheses, baseline-first "
  "modelling, leakage-safe validation, governance of data, attention to ethics, and a plan for monitoring and "
  "scaling. By committing in advance to measures of success and to an order for cutting scope, the plan "
  "reduces the chance of unplanned compromises and gives a reviewer a firm basis for judging the work.")

# ---------------- References ----------------
H1("References and Resources")
bullets(["Chapman, P. et al. (2000). <i>CRISP-DM 1.0: Step-by-step data mining guide.</i> CRISP-DM Consortium.",
         "Studer, S. et al. (2021). Towards CRISP-ML(Q): A machine learning process model with quality assurance "
         "methodology. <i>Machine Learning and Knowledge Extraction</i>, 3(2).",
         "Hersbach, H. et al. (2020). The ERA5 global reanalysis. <i>Quarterly Journal of the Royal "
         "Meteorological Society</i>, 146(730). Data via the Copernicus Climate Data Store.",
         "Central Pollution Control Board, India. National Air Quality Index and continuous ambient air quality "
         "monitoring data; national open data portal (data.gov.in).",
         "NASA Fire Information for Resource Management System (FIRMS), active fire data.",
         "Ke, G. et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. <i>Advances in Neural "
         "Information Processing Systems</i> 30.",
         "Lundberg, S. and Lee, S. (2017). A unified approach to interpreting model predictions. <i>Advances in "
         "Neural Information Processing Systems</i> 30.",
         "Hyndman, R. and Athanasopoulos, G. <i>Forecasting: Principles and Practice</i> (3rd ed.), OTexts.",
         "Mitchell, M. et al. (2019). Model cards for model reporting. <i>Proceedings of FAT* 2019</i>.",
         "Government of India (2023). The Digital Personal Data Protection Act, 2023."])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2 * cm, 1.2 * cm, "AirCast India - AI Project Plan")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                        bottomMargin=2 * cm, title="AI Project Plan - AirCast India",
                        author="Ansh Parashar", subject="Week 1 AI Project Planning and Documentation")
doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("built")
