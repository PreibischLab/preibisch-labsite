#!/bin/bash

RECIPIENTS="Stephan.Preibisch@mdc-berlin.de, Klim.Kolyvanov@mdc-berlin.de, Marwan.Zouinkhi@mdc-berlin.de, Dhana.Friedrich@mdc-berlin.de, Nikita.Vladimirov@mdc-berlin.de, Friedrich.Preusser@mdc-berlin.de, Laura.Breimann@mdc-berlin.de, bellonet@gmail.com"
##RECIPIENTS="bellonet@gmail.com"

SUBJECT="Update our website!"
BODY="Hi There Lab Buddies,\n\nYou've done some exciting stuff this past week - signed up for a conference, received a grant, published a paper, searched for/got a new lab member, organized a club/workshop, got cool new equipment, created a cool piece of software.. That's awesome! Now add it to the website.\n\nHere's the guide for how to do that:\nhttps://docs.google.com/document/d/1Zenmy1SIs_KmAJW0kx004rgXCqUkeB6qMcTYlneHQ_Q/edit?usp=sharing\n\nOr just email me and I will add it.\nHave a great day!\nAuto E"


/bin/echo -e "$BODY" | mail -s "$SUBJECT" ${RECIPIENTS}


