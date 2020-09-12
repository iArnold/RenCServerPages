# RenCServerPages
Code for processing Rebol Server Pages for REN-C

Put the executable r3 as renc (with chmod 755) in the cgi-bin directory.

Put the .htaccess file in a directory where the rencsp scripts will go (under).

Correct the rencsp.cgi to point to the cgi-bin directory of your site, then
put the renc.cgi in the directory as named in the .htaccess file.
Notice that you do not put it in the real cgi-bin directory, the example uses a 
regular directory called cgi.

Make sure the scripts are uploaded and set with correct rights (chmod 755).

Enjoy Ren-Csp pages!
