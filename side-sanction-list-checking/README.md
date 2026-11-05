# Side sanction list checking (KYC / AML helper)

Automate parts of comparing client names against the [UN SC Consolidated List](https://scsanctions.un.org/consolidated/) for Hong Kong company-secretary style workflows.

## Part 1 — download list snapshot

The consolidated “list” is published as an **HTML page** (the site offers “Print to PDF” in the browser). This repo saves that HTML for a given day so you can archive or pipe it into your own PDF/HTML tooling.

```bash
cd side-sanction-list-checking
pip install -r requirements.txt
python main.py
```

Output: `Part_1_Download_Sanction_List_from_the_Internet/downloads/UN_consolidated_list_YYYY-MM-DD.html`

**Note:** A previous script saved the page URL as `.pdf` by mistake; that produced invalid files. Use the HTML snapshot here, then convert with a browser or your PDF pipeline.

## Part 2–3 — PDF / dataframe / fuzzy match

- `Part_2-3_Analyse_and _Extract_the_Sanction_List_to_Dataframe/` — sample CSV, Jupyter PDF work  
- Excel fuzzy matching is described in the original workflow notes; implement or adapt with `rapidfuzz` / `fuzzywuzzy` as needed.

## Requirements

See `requirements.txt` (`requests`, `pandas`, PDF libraries, etc., depending on which parts you run).

## References

- UN consolidated list: https://scsanctions.un.org/consolidated/  
- Fuzzy lookup discussion (Excel): https://www.mrexcel.com/board/threads/fuzzy-matching-new-version-plus-explanation.195635/post-955137  
