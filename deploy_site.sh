cd /home/ella/preibisch-labsite;
git add _extras/bimsb_seminar.html;
git commit -m "automatic commit - bimsb_seminar";
git push;
git pull;
jekyll build;
rsync -r --progress _site/* ebahry@mdcuserweb.mdc-berlin.net:/var/www/html/004_preibischlab/
