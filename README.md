## simple-gallery
simple gallery is a single site for WordPress ngg-gallery pictures

sample at: http://gallery.tangcu.biz/


## dependencies
MySQL database of WordPress ngg-gallery (https://wordpress.org/plugins/nextgen-gallery/)

## requirement
> * Python 2.6+
> * pip requirement file: requirement

## config for server
Modify config.py to the value for runtime.
```
$albums_ids       #albums list display at first level menu
$serial_gallery   #gallery album play in order, default: []
$db_host          #host of WordPress database, default: localhost
$db_port          #port of WordPress database, default: 3306
$db_dbname        #dbname of WordPress database
$db_user          #user of WordPress database, default: ""
$db_password      #password of WordPress database, default: ""
$base_path        #base url of WordPress photo site, default: http://photo.tangcu.biz/
```

## run the server

```
python server_bottle.py
```

## run with docker

build image
```
docker build . -t simple-gallery-docker
```

run container
```
docker run -d --name=simple-gallery \
    --net=wordpress-photo-net \
    -e db_host=wordpress-mysql \
    -e albums_ids="[7,9,10,11]" \
    -e serial_gallery="[96,98]" \
    -e db_user="" \
    -e db_password="" \
    -e db_dbname=wpphoto \
    -e base_path="http://photo.tangcu.biz/" \
    -p 8030:8030  simple-gallery-docker
```

Licensed under the Apache License, Version 2.0. author zhmocean
