# CineLake - Phase 1: Business Understanding & Requirements

## Objective

Build a Movie & TV Analytics Lakehouse Platform capable of answering analytical questions about movies, TV series, actors, directors, writers, genres, ratings, popularity, and entertainment industry trends using IMDb datasets.

The platform should support analytics, search, filtering, sorting, drill-down exploration, and interactive dashboards.

---

# Business Goals

The primary goal of CineLake is to transform raw IMDb datasets into actionable insights through a modern lakehouse architecture.

The platform should enable users to:

* Discover movies and TV shows
* Analyze ratings and popularity
* Explore actor and director performance
* Analyze genre trends
* Track entertainment industry growth
* Search and filter content efficiently
* Perform self-service analytics

---

# Domain 1: Movie Analytics

## Ratings & Popularity

1. What are the highest-rated movies of all time?
2. What are the most voted movies of all time?
3. Which movies have the highest ratings with at least 10,000 votes?
4. Which movies have the highest ratings with at least 100,000 votes?
5. Which movies are underrated (high ratings but low vote counts)?
6. Which movies are overrated (high votes but lower ratings)?
7. What is the average movie rating across IMDb?

---

## Release Trends

8. How many movies were released each year?
9. Which year had the highest number of movie releases?
10. How has movie production changed over time?
11. Which decade produced the most movies?
12. What is the growth trend of movie releases?

---

## Runtime Analysis

13. What is the average movie runtime?
14. Which movies have the longest runtime?
15. Which movies have the shortest runtime?
16. How has movie runtime evolved over time?
17. What is the average runtime by genre?

---

# Domain 2: Genre Analytics

18. Which genres have the highest average ratings?
19. Which genres have the most movies?
20. Which genres receive the most votes?
21. What are the top-rated movies in each genre?
22. Which genres are growing fastest over time?
23. Which genres are declining over time?
24. What genres dominate each decade?
25. Which genres have the longest average runtime?
26. Which genres have the shortest average runtime?

---

# Domain 3: Actor Analytics

27. Which actors appear in the most movies?
28. Which actors appear in the highest-rated movies?
29. Which actors have the highest average movie ratings?
30. Which actors have the most movies with ratings above 8.0?
31. Which actors have worked across the most genres?
32. Which actors have the longest careers?
33. Which actors are most active by decade?
34. Which actors have the highest total vote count across all movies?

---

# Domain 4: Director Analytics

35. Which directors have directed the most movies?
36. Which directors have the highest average ratings?
37. Which directors have the most highly-rated movies?
38. Which directors have the highest cumulative vote count?
39. Which directors are most active by decade?
40. Which directors specialize in specific genres?
41. Which directors have the most consistent ratings?

---

# Domain 5: Writer Analytics

42. Which writers have contributed to the most titles?
43. Which writers have the highest average ratings?
44. Which writers have the most highly-rated movies?
45. Which writer-director combinations occur most frequently?

---

# Domain 6: TV Series Analytics

46. What are the highest-rated TV series?
47. What are the most voted TV series?
48. Which TV series have the most episodes?
49. Which TV series have the most seasons?
50. Which TV series have the highest average episode ratings?
51. Which TV series have the longest run?
52. Which TV genres are most popular?

---

# Domain 7: Episode Analytics

53. Which episodes have the highest ratings?
54. Which episodes received the most votes?
55. What is the average number of episodes per season?
56. Which TV series has the most episodes?
57. Which season has the highest average ratings?

---

# Domain 8: People Analytics

58. How many unique people exist in IMDb?
59. What are the most common professions?
60. Which people are known for the largest number of titles?
61. What is the distribution of professions across IMDb?

---

# Domain 9: Country & Language Analytics

62. Which titles are available in the most regions?
63. Which languages appear most frequently?
64. Which countries have the largest number of localized titles?
65. Which titles have the most alternative names?

---

# Domain 10: Entertainment Industry Trends

66. How has movie production changed since 1900?
67. How has TV production changed over time?
68. How have audience ratings changed over decades?
69. How has average runtime changed over decades?
70. Which genres dominated each decade?
71. How has content volume evolved over time?

---

# Domain 11: Search & Discovery

## Search Capabilities

72. Search movie details by title.
73. Search actor filmography.
74. Search director filmography.
75. Search TV series details.
76. Search writer details.
77. Display cast and crew for a title.

---

## Filter Capabilities

78. Filter movies by genre.
79. Filter movies by release year.
80. Filter movies by rating range.
81. Filter movies by vote count range.
82. Filter movies by runtime range.
83. Filter movies by language.
84. Filter movies by title type.
85. Filter actors by profession.
86. Filter directors by genre specialization.
87. Filter TV series by number of seasons.
88. Filter TV series by episode count.

---

## Sort Capabilities

89. Sort movies by rating.
90. Sort movies by vote count.
91. Sort movies by release year.
92. Sort movies by runtime.
93. Sort actors by movie count.
94. Sort actors by average rating.
95. Sort directors by movie count.
96. Sort directors by average rating.
97. Sort TV series by rating.
98. Sort TV series by episode count.

---

## Drill-Down Analytics

99. Navigate from Genre → Movies.
100. Navigate from Director → Movies.
101. Navigate from Actor → Filmography.
102. Navigate from TV Series → Seasons → Episodes.
103. Navigate from Movie → Cast & Crew.
104. Navigate from Movie → Director Profile.
105. Navigate from Movie → Similar Genre Movies.

---

## Dashboard Features

106. Multi-select Genre Filter.
107. Multi-select Year Filter.
108. Interactive Search Bar.
109. Dynamic Sorting.
110. Pagination for Large Result Sets.
111. Export Results to CSV.
112. Bookmark Favorite Searches.

---

# Domain 12: Executive KPI Dashboard

113. Total Movies
114. Total TV Series
115. Total Episodes
116. Total Actors
117. Total Directors
118. Total Writers
119. Total Votes
120. Average Rating
121. Total Genres
122. Total Languages
123. Total Regions

---

# Stretch Analytics (Future Enhancements)

124. Actor Success Score
125. Director Success Score
126. Genre Diversity Score
127. Movie Popularity Score
128. Career Longevity Index
129. Director Consistency Index
130. Genre Growth Index
131. Decade Popularity Index
132. TV Series Engagement Score
133. Franchise Influence Score
134. Audience Sentiment Proxy
135. IMDb Content Growth Forecast

---

# Expected Dashboard Pages

1. Overview Dashboard
2. Movie Analytics
3. Genre Analytics
4. Actor Analytics
5. Director Analytics
6. Writer Analytics
7. TV Series Analytics
8. Episode Analytics
9. Search & Discovery
10. KPI Dashboard

---

# Phase 1 Deliverables

## Business Documents

* Business Requirement Document (BRD)
* KPI Definitions
* Analytics Requirements
* Search Requirements
* Filter Requirements
* Sorting Requirements
* Dashboard Requirements

## Success Criteria

The platform should be capable of answering all defined business questions using the IMDb datasets.

---
