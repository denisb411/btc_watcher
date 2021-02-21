# btc_watcher
A bitcoin watcher to detect price falls and warn


## Usage

- Insert necessary data on `config.yml` file. 
    - Current only tested with Gmail. Needs to set account to 'less safe' mode.
- Execute
```bash
pip install -r requirements.txt
python run.py
```

- Or using Docker:
```bash
docker-compose up -d --build
```