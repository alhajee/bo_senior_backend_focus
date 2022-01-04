BMAT Back Office Senior Web Developer Test: Backend Focus
=========================================================

## Contents

* Some Context
* Running the Stack
* Part 1 - Creating an API
* Part 2 - File Ingestion
* Part 3 - Questions

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
* `iswc` - International Standard Musical Work Code, it’s a musical work identifier.
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
