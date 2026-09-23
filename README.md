# traceboard

A governance dashboard for Perplexity that traces assets from design file to live code across product surfaces. Built with Python and Streamlit.

## Features

- **Design token governance** — Track and validate tokens across components and surfaces.
- **Component standards** — Enforce consistent patterns and accessibility rules.
- **Asset tracing** — Link design artifacts to implementation and deployment.
- **Quality checks** — Run automated checks across multiple product surfaces.

## Local development

### Requirements

- Python 3.10 or later
- `pip`

### Setup

```bash
git clone https://github.com/FriesRdBest/traceboard.git
cd traceboard
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
