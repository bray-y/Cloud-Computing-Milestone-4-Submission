# OTU Cloud Computing - Milestone 4 Design Repository
### *Produced by Bralyn Loach-Perry*
#### *Ontario Tech Student ID: 100867075*

This repository contains the working code designed for the design portion of the milestone assignment as shown in my demo video.

<ins>The Design is broken into three parts:</ins>

1. **FilterReading Service** - `filter_reading.py` 
   - Eliminates records with missing measurements (`None`).  
   - Ensures only valid readings are passed to subsequent services.
   - accomodating `requirements.txt` file to ensure proper libraries are installed

2. **ConvertReading Service** - `convert_reading.py`  
   - Converts pressure and temperature units:  
     - Pressure: `P(psi) = P(kPa) / 6.895`  
     - Temperature: `T(F) = T(C) * 1.8 + 32`
     - accomodating `requirements.txt` file to ensure proper libraries are installed


3. **BigQuery Subscription** -  - `bq_reading.py` 
   - Preprocessed readings are automatically stored in a **BigQuery table** for downstream analysis.  
   - accomodating `requirements.txt` file to ensure proper libraries are installed
