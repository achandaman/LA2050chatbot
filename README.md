# LA2050 Chatbot

The LA2050 Navigator project is crucial for enhancing user engagement and accessibility within the [Ideas Hub](https://la2050.org/ideas), aligning with the Goldhirsh Foundation's mission to support impactful community initiatives. 

The chatbot will streamline donor and volunteer efforts by improving navigation and resource discovery, increasing support for local nonprofits, and amplifying their community impact. It may also be a framework for other non-profits, amplifying giving throughout the state and nation.

## Challenge Summary

Goldhirsh Foundation's LA2050 Ideas Hub project aims to create a chatbot that enhances user experience by facilitating navigation within the Ideas Hub using a hybrid search approach combining both keyword and semantic search.

### Desired Outcomes

The chatbot will assist visitors in identifying specific nonprofits to donate to, learn about, or volunteer with, along with for-profit companies and government entities who also submitted proposal solutions, while prioritizing nonprofits awarded by the Goldhirsh Foundation, those with multiple proposal submissions, and those in good standing with the IRS.

## Timeline

**Step 1: Research & Planning (1-2 week)**
- Study the database schema and identify necessary NLP techniques. 

**Step 2: Setting Up Tech Stack & Data Preprocessing (1 week)**
- Install necessary libraries, integrate the database with LangChain, and set up models.

**Step 3: Prototyping (2 weeks)**
- Develop a simple prototype that can handle basic questions.

**Step 4: Testing & Refinement (4 weeks)**
- Test on different query types, optimize responses and add more functionality.

**Step 5: Scaling Functionality (2 Week)**
- Refine the chatbot to ensure it can handle high user loads and more detailed queries, optimizing its performance for real-world use.

**Step 6: Final Deployment (1 week)**
- Deploy and monitor performance.

**Step 7: Presentation**
- Present our findings and the final product

## Project Organization
```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    │    
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations 
    │
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── __init__.py 
```

--------
