# CineLake - Phase 2: Source System Analysis

Status: ✅ COMPLETED

## Objective

Analyze IMDb source datasets, understand relationships, identify keys, define cardinality, and map datasets to business requirements.

The output of this phase will be used to design the Gold Layer dimensional model in Phase 3.

---

# Source System Overview

IMDb provides 7 datasets in TSV.GZ format.

All files:

* UTF-8 encoded
* Tab-separated
* GZIP compressed
* Use '\N' to represent NULL values

---

# Dataset Inventory

## 1. title.basics.tsv.gz

### Purpose

Master title dataset containing movies, TV series, TV episodes, shorts and other title types.

### Primary Key

```text
tconst
```

### Important Columns

| Column         | Description                              |
| -------------- | ---------------------------------------- |
| tconst         | Unique Title ID                          |
| titleType      | Movie, TV Series, TV Episode, Short, etc |
| primaryTitle   | Display title                            |
| originalTitle  | Original language title                  |
| isAdult        | Adult content flag                       |
| startYear      | Release year                             |
| endYear        | TV Series end year                       |
| runtimeMinutes | Runtime                                  |
| genres         | Up to 3 genres                           |

### Business Domains

* Movie Analytics
* Genre Analytics
* TV Analytics
* Search & Discovery

---

## 2. title.ratings.tsv.gz

### Purpose

IMDb ratings and popularity metrics.

### Primary Key

```text
tconst
```

### Important Columns

| Column        | Description     |
| ------------- | --------------- |
| tconst        | Unique Title ID |
| averageRating | IMDb Rating     |
| numVotes      | Vote Count      |

### Business Domains

* Movie Analytics
* Popularity Analytics
* Genre Analytics

---

## 3. title.crew.tsv.gz

### Purpose

Director and writer mapping.

### Primary Key

```text
tconst
```

### Important Columns

| Column    | Description  |
| --------- | ------------ |
| tconst    | Title ID     |
| directors | Director IDs |
| writers   | Writer IDs   |

### Business Domains

* Director Analytics
* Writer Analytics

---

## 4. title.principals.tsv.gz

### Purpose

Cast and crew participation dataset.

### Primary Key

```text
(tconst, ordering)
```

### Important Columns

| Column     | Description                            |
| ---------- | -------------------------------------- |
| tconst     | Title ID                               |
| ordering   | Ordering Number                        |
| nconst     | Person ID                              |
| category   | Actor, Actress, Director, Producer etc |
| job        | Job Name                               |
| characters | Character Names                        |

### Business Domains

* Actor Analytics
* Cast Analytics
* Search & Discovery

---

## 5. title.episode.tsv.gz

### Purpose

TV Series and Episode relationship dataset.

### Primary Key

```text
tconst
```

### Important Columns

| Column        | Description    |
| ------------- | -------------- |
| tconst        | Episode ID     |
| parentTconst  | TV Series ID   |
| seasonNumber  | Season Number  |
| episodeNumber | Episode Number |

### Business Domains

* TV Analytics
* Episode Analytics

---

## 6. title.akas.tsv.gz

### Purpose

Alternative titles, regions and languages.

### Primary Key

```text
(titleId, ordering)
```

### Important Columns

| Column          | Description            |
| --------------- | ---------------------- |
| titleId         | Title ID               |
| title           | Localized Title        |
| region          | Country/Region         |
| language        | Language               |
| types           | Alternative Title Type |
| attributes      | Additional Attributes  |
| isOriginalTitle | Original Title Flag    |

### Business Domains

* Country Analytics
* Language Analytics
* Search & Discovery

---

## 7. name.basics.tsv.gz

### Purpose

Master person dataset.

### Primary Key

```text
nconst
```

### Important Columns

| Column            | Description       |
| ----------------- | ----------------- |
| nconst            | Person ID         |
| primaryName       | Person Name       |
| birthYear         | Birth Year        |
| deathYear         | Death Year        |
| primaryProfession | Top 3 Professions |
| knownForTitles    | Famous Titles     |

### Business Domains

* Actor Analytics
* Director Analytics
* Writer Analytics
* People Analytics

---

# Key Relationships

## Movie ↔ Rating

```text
title.basics.tconst
        =
title.ratings.tconst
```

Cardinality:

```text
1 : 1
```

---

## Movie ↔ Crew

```text
title.basics.tconst
        =
title.crew.tconst
```

Cardinality:

```text
1 : Many
```

Multiple directors and writers can exist.

---

## Movie ↔ Cast

```text
title.basics.tconst
        =
title.principals.tconst
```

Cardinality:

```text
1 : Many
```

A movie contains many cast members.

---

## Person ↔ Cast

```text
name.basics.nconst
        =
title.principals.nconst
```

Cardinality:

```text
Many : Many
```

Actors can appear in many movies.

Movies can have many actors.

---

## Person ↔ Director

```text
name.basics.nconst
        =
title.crew.directors
```

Cardinality:

```text
Many : Many
```

---

## Person ↔ Writer

```text
name.basics.nconst
        =
title.crew.writers
```

Cardinality:

```text
Many : Many
```

---

## TV Series ↔ Episode

```text
title.basics.tconst
        =
title.episode.parentTconst
```

Cardinality:

```text
1 : Many
```

One TV series contains many episodes.

---

## Title ↔ Region / Language

```text
title.basics.tconst
        =
title.akas.titleId
```

Cardinality:

```text
1 : Many
```

One title can have many localized versions.

---

# Source System Relationship Diagram

```text
                  title.basics
                        |
        +---------------+----------------+
        |               |                |
        |               |                |
  title.ratings   title.crew    title.principals
        |               |                |
        |               |                |
        |               |           name.basics
        |               |
        |          name.basics
        |
        |
   title.episode
        |
        |
   parentTconst
        |
   TV Series

title.akas
    |
    |
titleId
    |
title.basics
```

---

# Source to Business Mapping

| Business Area      | Source Tables                                           |
| ------------------ | ------------------------------------------------------- |
| Movie Analytics    | title.basics, title.ratings                             |
| Genre Analytics    | title.basics, title.ratings                             |
| Actor Analytics    | title.principals, name.basics, title.ratings            |
| Director Analytics | title.crew, name.basics, title.ratings                  |
| Writer Analytics   | title.crew, name.basics                                 |
| TV Analytics       | title.episode, title.basics, title.ratings              |
| Episode Analytics  | title.episode, title.ratings                            |
| Country Analytics  | title.akas                                              |
| Language Analytics | title.akas                                              |
| Search & Discovery | title.basics, title.principals, name.basics, title.akas |

---

# Candidate Dimensions (Phase 3)

## dim_movie

Source:

```text
title.basics
```

---

## dim_person

Source:

```text
name.basics
```

---

## dim_date

Source:

```text
startYear
```

---

# Candidate Facts (Phase 3)

## fact_movie_rating

Sources:

```text
title.basics
title.ratings
```

---

## fact_cast

Sources:

```text
title.principals
name.basics
```

---

## fact_director

Sources:

```text
title.crew
name.basics
```

---

## fact_episode

Sources:

```text
title.episode
title.basics
```

---

# Deliverables

* Dataset Analysis
* Relationship Mapping
* Cardinality Analysis
* Source-to-Business Mapping
* Candidate Fact Tables
* Candidate Dimension Tables

---
