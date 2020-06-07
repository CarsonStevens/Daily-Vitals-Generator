# Daily-Vitals-Generator
The purpose of this project was to create a daily, auto-generated newsletter that sparks conversation and community building. The intended audience is for nursing home, treatment/medical centers, or anywhere building a sense of community is important. A 'Daily Vital' contains things from the weather, This Day in History, riddles, horoscopes, multiple types of word games, and more. The project is run on a Flask server that runs a CRON job at midnight to update the page. Although most the information is scraped from websites, several generators were made to make sure that the games are fresh. The Hink Pink Generator, for example, takes two words and then finds two words that would mean the same thing, but also rythme. The generators are also tunable for difficulty and uses the NLTK library to check produced challenges against a word Corpus for viability. Users can also enter custom parameters to generate their own newsletters and a content submission area allows users to share their own game questions and answers to be used in future newsletters.
