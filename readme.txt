

ALTER USER postgres WITH PASSWORD 'newpassword';
Say, via a psql -c command:

sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'newpassword';"

stopped - GETting a single post