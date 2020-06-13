import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp("He went to play basketball")
print(nlp.pipe_names)


frasi = list()
frasi.append("Stuart John \"Woolly\" Wolstenholme (15 April 1947 – 13 December 2010) was a vocalist and keyboard player with the British progressive rock band Barclay James Harvest.")
frasi.append("Lee Hye-Ryeon (이혜련), name changed to Heo Yun (허윤), best known as U;Nee (Korean: 유니; May 3, 1981 – January 21, 2007), was a South Korean singer, rapper, dancer and actress.")
frasi.append("Ellen Joyce Loo Hoi Tung (Chinese: 盧凱彤; Jyutping: Lou4 Hoi2tung4; 27 March 1986 – 5 August 2018) was a Canadian-Hong Kong musician, singer-songwriter and record producer.")
frasi.append("Stuart John \"Woolly\" Wolstenholme (15 April 1947 – 13 December 2010) was a vocalist and keyboard player with the British progressive rock band Barclay James Harvest.")
frasi.append("Peter William Ham (27 April 1947 – 24 April 1975) was a Welsh singer, songwriter and guitarist, best known as a lead vocalist of and composer for the 1970s rock band Badfinger, whose hit songs include \"No Matter\"")
frasi.append("was a reggae singer who enjoyed considerable chart success in Jamaica and in")
frasi.append("Donny Edward Hathaway (October 1, 1945 – January 13, 1979) was an American soul singer, keyboardist, songwriter, and arranger.")
frasi.append("Richard George Manuel (April 3, 1943 – March 4, 1986) was a Canadian composer, singer, and multi-instrumentalist, best known as a pianist and lead singer of The Band.")
frasi.append("Violeta del Carmen Parra Sandoval (Spanish pronunciation: [bjoˈleta ˈpara]; 4 October 1917 – 5 February 1967) was a Chilean composer, singer-songwriter, folklorist, ethnomusicologist and visual artist")
frasi.append("Megadeth was a heavy metal band/power metal")
#for frase in frasi: single_test(frase)