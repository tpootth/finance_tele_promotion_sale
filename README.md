# finance_tele_promotion_sale — Bank Call Prioritization

ใครควรได้รับสายเสนอเงินฝากประจำก่อน โทรกี่ราย กี่ครั้ง ผ่านช่องทางไหน — โมเดลจัดอันดับรายชื่อ + สถานการณ์ธุรกิจ บนข้อมูล [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) (41,188 รายการ, โปรตุเกส 2008–2010)

**Dashboard:** https://tpootth.github.io/finance_tele_promotion_sale/

## How it works

Every push to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

1. Executes `Bank_Model_Storytelling.ipynb` from scratch (~2–3 min), which regenerates every table and figure in `results_model_and_business/`
2. Renders the executed notebook to HTML
3. `site/build_site.py` turns the result CSVs into an interactive dashboard (`site/template.html`, Plotly)
4. Deploys to GitHub Pages; the executed notebook + results are also kept as a run artifact

## Files

| Path | What |
|---|---|
| `Bank_Model_Storytelling.ipynb` | Main notebook (story order, chapters 1–6 + appendix) |
| `bank-additional-full.csv` | UCI data (the notebook downloads it if missing) |
| `results_model_and_business/` | Outputs from the last local run (CI regenerates them) |
| `site/` | Dashboard generator, template and vendored JS (Plotly, marked) |
| `requirements.txt` | Pinned versions — pandas 3.x breaks the notebook |

## Run locally

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute Bank_Model_Storytelling.ipynb --output-dir build --output executed
jupyter nbconvert --to html build/executed.ipynb --output-dir build --output notebook
python site/build_site.py --notebook-html build/notebook.html
open _site/index.html
```

ทุกข้อเป็นความสัมพันธ์จากข้อมูลย้อนหลัง ตัวเลขเงินเป็นสมมติฐานเพื่อประกอบการอธิบาย ยังไม่ใช่ผลเชิงเหตุ
