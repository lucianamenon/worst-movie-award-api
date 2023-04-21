# start by pulling the python image
FROM python:3.10-buster

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

CMD exec gunicorn -b 0.0.0.0:5000 main:app --timeout 60

#CMD [ "python", "./main.py" ]