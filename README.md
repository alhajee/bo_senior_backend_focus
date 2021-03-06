BMAT Back Office Senior Web Developer Test: Backend Focus
=========================================================

## Contents

* [Solution](#solution)
* [Setup](#setup)
* [Some Context](#some-context)
* [Running the Stack](#running-the-stack)
* [Part 1 - Creating an API](#part-1---creating-an-api)
* [Part 2 - File Ingestion](#part-2---file-ingestion)
* [Part 3 - Questions](#part-3---questions)


# Solution

## Models
- In order to avoid replicating contributors, I created a seperate model that stores <br>
contributors and linked them to a musical work using `many-to-many` relationship. <br>
This way, a contributor only has to be created once

## Serializers
- Created a custom serializer to join `count`, `work` and `file` together

## URLs
- Created two API routes, one to handle `files` and the other when `works` is present in query

## FileIngestion
- Created a `django management command` that Ingests large files in batch using <br>
`through` & `bulk create` for improved performance 
<!-- * SingleView -->

## Answer to questions

1. If two files provide `conflicting information` on the same work, the reasonable thing to do is <br> 
`ignore the fields they have in common`, and `merge the fields they differ`, since it is highly <br>
likely that both sources are correct

2. The endpoints described in this assignment woulld not suffice to provide a `SingleView`, because it is highly <br>
dependant on the file/source. A SingleView can simply take a unique identifier for a work (work ID) to query <br>
all information related to that particular work

3. With a SingleView that contains at least `20 million musical work`, the API will suffer from `low response time`<br>
due to the `query size`, But a solution would be to Implement `caching` and also `pagination` to limit the <br>
query size in a single request


# Setup

1. Deploy docker containers using the `docker-compose.yaml` and `Dockerfile`.
```bash
docker-compose up --build
```

2. Make database migrations
```bash
docker-compose exec api python manage.py migrate
```

3. Ingest all three csv files
```bash
docker-compose exec api python manage.py load_csv -f sony.csv universal.csv warner.csv
```

4. Run unit tests & integration tests
```bash
docker-compose exec api python manage.py test repertoire.tests
```

5. Access the API endpoints through
```bash
http://<host_machine_ip>:8000/files
```


## Some context

BMAT's Back Office team develops back office tools where CMOs (Collective Management Organizations - in most cases, not-for-profit entities, that manage rights on behalf of their members) can go about their daily operations. One of the most important operations is the management of musical works documentation (or works for short). Note here that we work with metadata rather than audio. A musical work consists of the musical notes and lyrics (if any) in a musical composition. A musical work may be fixed in any form, such as
a piece of sheet music or a sound recording, but it's usually represented by metadata like: title, contributors, roles, duration, etc.

Metadata can stem from different sources and be provided in different formats and some sources may provide incomplete information. The final aim is to have a unique, consolidated, complete and up-to-date picture of each musical work, to build what we call a SingleView.

As part of managing repertoire, it's important to have a clear vision of which sources of documentation (mainly files) were provided to the system and which musical works were described in each file.

## Running the Stack

In order to run this test you'll need `docker-compose`. We provide a Docker Compose file that you will use to run the stack (Django with DRF, with a postgres DB). If you're curious, you can review the process we used to set up this basic Docker + Django project as described in the following link:

https://docs.docker.com/samples/django/

Running `docker-compose up` should be enough, but if you run into any trouble with permissions please review the process outlined in the previous link as you may find a solution for your particular environment.

## Part 1 - Creating an API

You'll be creating an API using Django Rest Framework as defined in the `openapi.json` file next to this README. You can access a live documentation in http://localhost:8001.

Pay close attention to the endpoint definitions and payload, as you will be evaluated on how closely you can implement the API according to the specification.

For this part you'll need to implement:
* Models
* Serializers
* URLs
* Views

Bear in mind that **some type of testing is expected.**

## Part 2 - File Ingestion

In the `/files` folder you'll find three CSV files. These files describe different works (Note that some of them describe the same musical work, but with some differences - see Part 3).

Your aim in this part is to read the files into the system and parse their content. Each file contains the following columns:

* `title` - The Title of the Musical Work
* `contributors` - Work contributors such as composers, lyricists, etc. we skip the role for simplicity. There can be multiple contributors, they are separated by |
* `iswc` - International Standard Musical Work Code, it???s a musical work identifier.
* `source` - The name of the metadata provider.
* `proprietary_id` - Identifier used by the metadata provider.

Note that these colums map neatly to the Work schema in the `openapi.yml` file ;)

Feel free to do the parsing with any library of your liking, but do:

* Remember to update the `requirements.txt` file
* Provide a django management command to trigger the ingestion.

If you manage to ingest the three files provided, you'll be able to use the API you created in part 1 to retreive the list of files and the metadata contained in each. Neat!

## Part 3 - Questions

* As mentioned in the context section, the final aim of metadata ingestion is to create a SingleView. What could be doone if two files provide conflicting information on the same work?

* Could you use the endpoints described in this assignment or would have to create some new endpoints to provide the works of the SingleView?

* Imagine that the Single View has 20 million musical works, do you think your solution would have a similar response time? What technologies would you use to keep response times reasonable?
