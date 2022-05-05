# Articholic

## Resource

**Articles**

*Attributes*:

* title (string)
* author (string)
* code (string)
* content (string)

## Schema

```sql
CREATE TABLE Articles (
id INTEGER PRIMARY KEY,
title TEXT,
author TEXT,
code TEXT,
content TEXT);
```

## REST Endpoints

Name                  | Method | Path
----------------------|--------|------------------
Retrieve All Articles | GET    | /articles
Retrieve An Article   | GET    | /articles/*\<id\>*
Create An Article     | POST   | /articles
Update An Article     | PUT    | /articles/*\<id\>*
Delete An Article     | DELETE | /articles/*\<id\>*


**Users**

*Attributes*:

* username (string)
* password (string)
* firstname (string)
* lastname (string)

## Schema

```sql
CREATE TABLE Users (
id INTEGER PRIMARY KEY,
username TEXT,
password TEXT,
firstname TEXT,
lastname TEXT);
```

## REST Endpoints

Name                  | Method | Path
----------------------|--------|------------------
Retrieve A User   | GET    | /articles/*\<username\>\<password\>*
Create A User     | POST   | /articles