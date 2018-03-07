#! /bin/sh

if [ -z "$albums_ids" ]; then
        export albums_ids="[7,9,10,11]"
fi
sed -i "s/\$albums_ids/$albums_ids/g" /data/gallery/config.py

if [ -z "$serial_gallery" ]; then
        export serial_gallery="[96,98]"
fi
sed -i "s/\$serial_gallery/$serial_gallery/g" /data/gallery/config.py

if [ -z "$db_host" ]; then
        export db_host="localhost"
fi
sed -i "s/\$db_host/$db_host/g" /data/gallery/config.py

if [ -z "$db_port" ]; then
        export db_port="3306"
fi
sed -i "s/\$db_port/$db_port/g" /data/gallery/config.py

if [ -z "$db_user" ]; then
        export db_user=""
fi
sed -i "s/\$db_user/$db_user/g" /data/gallery/config.py

if [ -z "$db_password" ]; then
        export db_password=""
fi
sed -i "s/\$db_password/$db_password/g" /data/gallery/config.py

if [ -z "$db_dbname" ]; then
        export db_dbname=""
fi
sed -i "s/\$db_dbname/$db_dbname/g" /data/gallery/config.py


if [ -z "$base_path" ]; then
        export base_path="photo.tangcu.biz"
fi
sed -i "s/\$base_path/$base_path/g" /data/gallery/config.py
