FROM python:3

COPY ./main.py ./

COPY ./get_wikipedia_links.py ./

RUN pip install PyDictionary

RUN pip install --upgrade language_tool_python

CMD [ "python", "./main.py" ]
