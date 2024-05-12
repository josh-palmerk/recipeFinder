## Overview

**Project Title**: RecipeBase

**Project Description**: Basic mySQL GUI for interacting with a recipe database

**Project Goals**: Learn SQL syntax/formating, use tools from mySQL, learn pyQT, increase capability to manage generative AI use.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Build a mySQL database, any one you want.
2. Pull RecipeBase repository
3. Enter credentials in config.py in python dict format
4. Run main.py

Instructions for using the software:

1. Select table
2. Select Query type
3. Select columns to use in query (some queries only accept 1 column)
4. Enter data in text boxes (if applicable to query, box will appear)
5. Make sure to put ' ' around any string
6. Click execute to effectuate query

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* mySQL (Workbench recommended as well)
* Python 3.11
* pyQT (library)
* mySQL connector (library)

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Simply SQL Textbook](https://learning.oreilly.com/library/view/simply-sql)
* [ChatGPT](chat.openai.com)
* [mySQL.com](www.mysql.com)
* Intro to databases course from my university

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Input validation: some invalid inputs crash the program
* [ ] Checkbox area size = checkbox amt * height
* [ ] Modularize & encapsulate (organize code)
* [ ] Allow more flexible DB connection
* [ ] Reduce redundancy/repetitiveness in DB connection
