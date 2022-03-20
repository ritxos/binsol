FROM python:3.9
ADD solution.py /
RUN pip install prometheus_client  binance-connector
CMD [ "python", "-u", "./solution.py" ]