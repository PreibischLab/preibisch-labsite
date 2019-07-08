cd /home/ella/preibisch-labsite;
git add _extras/bimsb_seminar.html;
git add _external/lightsheet_workshop.html;
git commit -m "automatic commit - bimsb_seminar";
git push;
git pull;
jekyll build;
rsync -r --progress _site/* ebahry@preibischlab.mdc-berlin.de:/var/www/html/004_preibischlab/
