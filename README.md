Neko
====

Description
-----------

Simple web-based status board for Hudson and Jenkins.

Configuration
-------------

### Apache

The specifics of your configuration will depend on the location of your install but should look something like this:  


    <VirtualHost *:80>

      DocumentRoot /usr/share/neko/site/

      <Directory /usr/share/neko/site/>
        AllowOverride All
      </Directory>

      WSGIScriptAlias /api /usr/share/neko/api.wsgi

      LogLevel warn
      
    </VirtualHost>