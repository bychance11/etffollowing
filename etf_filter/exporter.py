# etf_filter/exporter.py

import pandas as pd
import os
from datetime import datetime
from config.settings import OUTPUT_FOLDER

def export_to_excel(results):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    df = pd.DataFrame(results)
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"filtered_{now}.xlsx"
    path = os.path.join(OUTPUT_FOLDER, filename)
    df.to_excel(path, index=False)
