# AI-EarthHack-WXW

## Run


### Prep Env & Install dependencies

```bash
conda create -n AI-earth python=3.12
conda activate AI-earth
pip install -r requirements.txt
```

### Replace the API key in the .env file

Create a file named `.env` and add the `OPENAI_API_KEY` to it.

### Run the app

```bash
sudo hupper -m streamlit run app.py
```
